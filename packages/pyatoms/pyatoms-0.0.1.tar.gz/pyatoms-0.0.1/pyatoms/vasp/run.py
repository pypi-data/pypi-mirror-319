import os
import pickle
import time
from os.path import join

from pymatgen.core.structure import Structure

from pyatoms.utils.bash import grep
from pyatoms.utils.file import backup, cp_r_atomic, get_tmp_path, rm_fr_atomic
from pyatoms.utils.loglib import get_file_logger
from pyatoms.vasp.errors import MaxTimeExceededError, VASPError
from pyatoms.vasp.inputs import INCAR
from pyatoms.vasp.outputs import OUTCAR


class VASPRelax:
    def __init__(
        self, 
        path_dir_input, 
        path_dir_run, 
        path_log, 
        server, 
        vasp_version, 
        run_vasp_func, 
        max_time=5, 
        start_from_wavecar={'on' : False}, 
        ngxyz_enhancing={'on' : False}, 
        ediffg_reducing={'on' : False}, 
    ):
        """
        start_from_wavecar:
            on
            transform_incar_from_relax_to_wavecar:
                None
                a function taking an INCAR instance as its first argument
            remove_wavecar
        ngxyz_enhancing:
            on
            start
            end
            step
            method:
                'adding'
                'scaling'
            factor
        ediffg_reducing:
            on
            start
            end
            step
            method:
                'adding'
                'scaling'
            factor
        """
        self.path_dir_input = path_dir_input
        self.path_dir_run = path_dir_run
        self.path_log = path_log
        self.server = server
        self.vasp_version = vasp_version
        self.run_vasp_func = run_vasp_func
        self.max_time = max_time
        self.start_from_wavecar = start_from_wavecar
        self.ngxyz_enhancing = ngxyz_enhancing
        self.ediffg_reducing = ediffg_reducing
        self.state = None
        
    def check(self):
        incar = INCAR()
        if not os.path.isfile(join(self.path_dir_run, 'INCAR')):
            path_incar = join(self.path_dir_input, 'INCAR')
        else:
            path_incar = join(self.path_dir_run, 'INCAR')
        incar.read_from_file(path_incar)
        nsw = int(incar.get_value('NSW'))
        lwave = incar.get_value('LWAVE')
        lcharg = incar.get_value('LCHARG')
        
        success_mark = ' reached required accuracy - stopping structural energy minimisation'
        zbrent_mark = '|      please rerun with smaller EDIFF, or copy CONTCAR                       |'
        nonconvergence_mark = '%4d F=' % (nsw)
        accounting_mark = ' General timing and accounting informations for this job:'
        
        if not os.path.isdir(join(self.path_dir_run)):
            self.state = 'not_started'
            return
        
        if (not os.path.isfile(join(self.path_dir_run, 'OUTCAR'))) or (not os.path.isfile(join(self.path_dir_run, 'vasp_out'))):
            self.state = 'outcar_or_vasp_out_not_found'
            return
        
        if grep(success_mark, join(self.path_dir_run, 'vasp_out')) != '':
            if grep(accounting_mark, join(self.path_dir_run, 'OUTCAR')) != '':
                self.state = 'finished'
                return
            else:
                if (lwave=='.TRUE.') or (lcharg=='.TRUE.'):
                    self.state = 'interrupted_writing_chgcar_or_wavecar'
                    return
                else:
                    raise VASPError(
                        'VASPRelax.check: success_mark: True, accounting_mark: False, lwave: False, lcharg: False'
                    )
        else:
            if grep(zbrent_mark, join(self.path_dir_run, 'vasp_out')) != '':
                self.state = 'zbrent_error'
                return
            
            if grep(nonconvergence_mark, join(self.path_dir_run, 'vasp_out')) != '':
                self.state = 'not_converged'
                return
            
            raise VASPError(
                'VASPRelax.check: success_mark: False, zbrent_mark: False, nonconvergence_mark: False'
            )
    
    def _backup_and_try_start_from_contcar(self, logger, counter_nonconvergence_related):
        path_dir_backup = backup(self.path_dir_run)
        logger.info('backup: %s' % (os.path.basename(path_dir_backup)))
        
        # ensure atomicity
        path_dir_run_tmp = get_tmp_path(self.path_dir_run)
        rm_fr_atomic(path_dir_run_tmp)
        os.mkdir(path_dir_run_tmp)
        for i in os.listdir(join(self.path_dir_input)):
            cp_r_atomic(join(path_dir_backup, i), join(path_dir_run_tmp, i))
        os.rename(path_dir_run_tmp, self.path_dir_run)
        
        try:
            Structure.from_file(join(path_dir_backup, 'CONTCAR'))
        except:
            counter_nonconvergence_related = 0
            cp_r_atomic(join(self.path_dir_input, 'POSCAR'), join(self.path_dir_run, 'POSCAR'))
            logger.info('CONTCAR bad, start from the original POSCAR')
            logger.info('counter_nonconvergence_related: 0')
        else:
            cp_r_atomic(join(path_dir_backup, 'CONTCAR'), join(self.path_dir_run, 'POSCAR'))
            logger.info('CONTCAR ok, start from the last CONTCAR')
        
        return path_dir_backup, counter_nonconvergence_related
    
    @staticmethod
    def transform_incar_from_relax_to_wavecar(
        incar, 
        nelm_scaling_factor=2.00, 
        ediff_scaling_factor=1E-01, 
    ):
        incar.set_how_to_start('start_from_scratch')
        incar.set_value('IBRION', -1)
        incar.set_value('ALGO', 'All')
        incar.del_value('ISIF')
        incar.set_value('NSW', 0)
        incar.set_value('NELM', int(int(incar.get_value('NELM'))*nelm_scaling_factor))
        incar.set_value('EDIFF', '%.2E' % (float(incar.get_value('EDIFF'))*ediff_scaling_factor))
        incar.del_value('EDIFFG')
        incar.set_value('LWAVE', '.TRUE.')
        
        return incar
        
    def run(self):
        logger = get_file_logger('vasp_relax', self.path_log)
        logger.info('---------- VASPRelax.run ----------')
        
        counter = 1
        counter_nonconvergence_related = 0
        restart_with_vasp_error = False
        try:
            self.check()
        except VASPError:
            restart_with_vasp_error = True
        
        while (counter<=self.max_time) and (self.state!='finished'):
            logger.info('--- counter: %d ---' % (counter))
            logger.info('state: %s' % (self.state))
            
            if self.state == 'not_started':
                cp_r_atomic(self.path_dir_input, self.path_dir_run)
            
            if (self.state in ['outcar_or_vasp_out_not_found', 'interrupted_writing_chgcar_or_wavecar']) or restart_with_vasp_error:
                path_dir_backup, counter_nonconvergence_related = self._backup_and_try_start_from_contcar(logger, counter_nonconvergence_related)
                
            if self.state in ['zbrent_error', 'not_converged']:
                counter_nonconvergence_related += 1
                logger.info('counter_nonconvergence_related: %d' % (counter_nonconvergence_related))
                
                path_dir_backup, counter_nonconvergence_related = self._backup_and_try_start_from_contcar(logger, counter_nonconvergence_related)
                
                if self.ngxyz_enhancing['on']:
                    start = self.ngxyz_enhancing['start']
                    step = self.ngxyz_enhancing['step']
                    end = self.ngxyz_enhancing['end']
                    method = self.ngxyz_enhancing['method']
                    factor = self.ngxyz_enhancing['factor']
                    
                    if ((counter_nonconvergence_related-start)%step==0) and (start<=counter_nonconvergence_related<end):
                        path_ngxyz = join(os.path.dirname(self.path_dir_run), 'ngxyz.pkl')
                        
                        if os.path.isfile(path_ngxyz):
                            with open(path_ngxyz, mode='rb') as f:
                                ngxyz = pickle.load(f)
                            ngx_0 = int(ngxyz['NGX'])
                            ngy_0 = int(ngxyz['NGY'])
                            ngz_0 = int(ngxyz['NGZ'])
                            
                            outcar = OUTCAR()
                            outcar.set_path_outcar(join(path_dir_backup, 'OUTCAR'))
                            ngxyz = outcar.get_ngxyz()
                            ngx = ngxyz['NGX']
                            ngy = ngxyz['NGY']
                            ngz = ngxyz['NGZ']
                            
                            if method == 'adding':
                                new_ngx = int(ngx + ngx_0 * factor)
                                new_ngy = int(ngy + ngy_0 * factor)
                                new_ngz = int(ngz + ngz_0 * factor)
                            elif method == 'scaling':
                                new_ngx = int(ngx * factor)
                                new_ngy = int(ngy * factor)
                                new_ngz = int(ngz * factor)
                            else:
                                raise ValueError(
                                    'VASPRelax.run: valid method: {\'adding\', \'scaling\'}, method: %s' % (method)
                                )
                            
                            incar = INCAR()
                            incar.read_from_file(join(self.path_dir_run, 'INCAR'))
                            incar.set_value('NGX', new_ngx)
                            incar.set_value('NGY', new_ngy)
                            incar.set_value('NGZ', new_ngz)
                            incar.write(join(self.path_dir_run, 'INCAR'))
                            
                            logger.info('ngx: %d, ngy: %d, ngz: %d, new_ngx: %d, new_ngy: %d, new_ngz: %d' % (ngx, ngy, ngz, new_ngx, new_ngy, new_ngz))
                
                if self.ediffg_reducing['on']:
                    start = self.ediffg_reducing['start']
                    step = self.ediffg_reducing['step']
                    end = self.ediffg_reducing['end']
                    method = self.ediffg_reducing['method']
                    factor = self.ediffg_reducing['factor']
                    
                    if ((counter_nonconvergence_related-start)%step==0) and (start<=counter_nonconvergence_related<end):
                        incar = INCAR()
                        incar.read_from_file(join(self.path_dir_input, 'INCAR'))
                        ediffg_0 = float(incar.get_value('EDIFFG'))
                        
                        incar = INCAR()
                        incar.read_from_file(join(path_dir_backup, 'INCAR'))
                        ediffg = float(incar.get_value('EDIFFG'))
                        
                        if method == 'adding':
                            new_ediffg = ediffg + ediffg_0 * factor
                        elif method == 'scaling':
                            new_ediffg = ediffg * factor
                        else:
                            raise ValueError(
                                'VASPRelax.run: valid method: {\'adding\', \'scaling\'}, method: %s' % (method)
                            )
                        
                        incar = INCAR()
                        incar.read_from_file(join(self.path_dir_run, 'INCAR'))
                        incar.set_value('EDIFFG', '%.2E' % new_ediffg)
                        incar.write(join(self.path_dir_run, 'INCAR'))
                        
                        logger.info('ediffg: %.2E, new_ediffg: %.2E' % (ediffg, new_ediffg))
            
            if self.start_from_wavecar['on']:
                logger.info('start_from_wavecar[\'on\']: True')
            
                path_dir_wavecar = join(self.path_dir_run, 'wavecar')
                os.mkdir(path_dir_wavecar)
                
                incar = INCAR()
                incar.read_from_file(join(self.path_dir_run, 'INCAR'))
                if self.start_from_wavecar['transform_incar_from_relax_to_wavecar'] != None:
                    incar = self.start_from_wavecar['transform_incar_from_relax_to_wavecar'](incar)
                    logger.info('transform INCAR from relax mode to wavecar mode (using user defined func)')
                else:
                    incar = self.transform_incar_from_relax_to_wavecar(incar)
                    logger.info('transform INCAR from relax mode to wavecar mode (using built-in func)')
                
                path_dir_input = join(path_dir_wavecar, 'input')
                
                # ensure atomicity
                path_dir_input_tmp = get_tmp_path(path_dir_input)
                rm_fr_atomic(path_dir_input_tmp)
                os.mkdir(path_dir_input_tmp)
                for i in os.listdir(self.path_dir_input):
                    cp_r_atomic(join(self.path_dir_run, i), join(path_dir_input_tmp, i))
                incar.write(join(path_dir_input_tmp, 'INCAR'))
                os.rename(path_dir_input_tmp, path_dir_input)
                
                vaspscf = VASPScf(
                    path_dir_input, 
                    path_dir_run=join(path_dir_wavecar, 'run'), 
                    path_log=join(path_dir_wavecar, 'log'), 
                    server=self.server, 
                    vasp_version=self.vasp_version, 
                    run_vasp_func=self.run_vasp_func, 
                    max_time=3, 
                    nelm_scaling_factor=2.00, 
                )
                logger.info('vaspscf.run() to get WAVECAR ...')
                vaspscf.run()
                
                os.rename(join(path_dir_wavecar, 'run', 'WAVECAR'), join(self.path_dir_run, 'WAVECAR'))
                logger.info('mv WAVECAR back to relax')
                
                incar = INCAR()
                incar.read_from_file(join(self.path_dir_run, 'INCAR'))
                incar.set_value('ISTART', 1)
                incar.set_value('ICHARG', 0)
                incar.write(join(self.path_dir_run, 'INCAR'))
                logger.info('adjust INCAR (for relax) to start from WAVECAR')
            
            os.chdir(self.path_dir_run)
            
            logger.info('VASP start ...')
            start_time = time.time()
            self.run_vasp_func[self.server][self.vasp_version]()
            end_time = time.time()
            logger.info('VASP runtime: %d s' % (end_time-start_time))
            
            counter += 1
            self.check()
            
            if self.start_from_wavecar['on']:
                if self.start_from_wavecar['remove_wavecar']:
                    rm_fr_atomic(join(self.path_dir_run, 'WAVECAR'))
                    logger.info('rm WAVECAR')
            
            try:
                path_ngxyz = join(os.path.dirname(self.path_dir_run), 'ngxyz.pkl')
                path_ngxyz_tmp = join(os.path.dirname(self.path_dir_run), 'ngxyz_tmp.pkl')
                
                if not os.path.isfile(path_ngxyz):
                    outcar = OUTCAR()
                    outcar.set_path_outcar(join(self.path_dir_run, 'OUTCAR'))
                    ngxyz = outcar.get_ngxyz()
                    
                    # this uses a two-step operation, first serializing the object to a temporary 
                    # file, then renaming it, to ensure the atomicity of the pickle serialization
                    with open(path_ngxyz_tmp, mode='wb') as f:
                        pickle.dump(ngxyz, f)
                    os.rename(path_ngxyz_tmp, path_ngxyz)
                    
                    logger.info('dump ngxyz.pkl')
            except:
                pass
            
        if (counter==(self.max_time+1)) and (self.state!='finished'):
            logger.info('max_time: %d, final state: %s' % (self.max_time, self.state))
            raise MaxTimeExceededError(
                'VASPRelax.run: max_time: %d' % (self.max_time)
            )
        
        logger.info('final state: %s' % (self.state))


class VASPScf:
    def __init__(
        self, 
        path_dir_input, 
        path_dir_run, 
        path_log, 
        server, 
        vasp_version, 
        run_vasp_func, 
        max_time=3, 
        nelm_scaling_factor=2.00, 
    ):
        self.path_dir_input = path_dir_input
        self.path_dir_run = path_dir_run
        self.path_log = path_log
        self.server = server
        self.vasp_version = vasp_version
        self.run_vasp_func = run_vasp_func
        self.max_time = max_time
        self.nelm_scaling_factor = nelm_scaling_factor
        self.state = None
    
    def check(self):
        success_mark = '1 F='
        nonconvergence_mark = '|     The electronic self-consistency was not achieved in the given           |'
        accounting_mark = ' General timing and accounting informations for this job:'
        
        incar = INCAR()
        incar.read_from_file(join(self.path_dir_input, 'INCAR'))
        lwave = incar.get_value('LWAVE')
        lcharg = incar.get_value('LCHARG')
        
        if not os.path.isdir(join(self.path_dir_run)):
            self.state = 'not_started'
            return
        
        if (not os.path.isfile(join(self.path_dir_run, 'OUTCAR'))) or (not os.path.isfile(join(self.path_dir_run, 'vasp_out'))):
            self.state = 'outcar_or_vasp_out_not_found'
            return
        
        if grep(success_mark, join(self.path_dir_run, 'vasp_out')) != '':
            if grep(nonconvergence_mark, join(self.path_dir_run, 'vasp_out')) == '':
                if grep(accounting_mark, join(self.path_dir_run, 'OUTCAR')) != '':
                    self.state = 'finished'
                    return
                else:
                    if (lwave == '.TRUE.') or (lcharg == '.TRUE.'):
                        self.state = 'interrupted_writing_chgcar_or_wavecar'
                        return
                    else:
                        raise VASPError(
                            'VASPScf.check: success_mark: True, nonconvergence_mark: False, accounting_mark: False, lwave: False, lcharg: False'
                        )
            else:
                self.state = 'not_converged'
                return
        else:
            raise VASPError(
                'VASPScf.check: success_mark: False'
            )
    
    def run(self):
        logger = get_file_logger('vasp_scf', self.path_log)
        logger.info('---------- VASPScf.run ----------')
        
        counter = 1
        restart_with_vasp_error = False
        try:
            self.check()
        except VASPError:
            restart_with_vasp_error = True
        
        while (counter<=self.max_time) and (self.state!='finished'):
            logger.info('--- counter: %d ---' % (counter))
            logger.info('state: %s' % (self.state))
            
            if self.state == 'not_started':
                cp_r_atomic(self.path_dir_input, self.path_dir_run)
            
            if (self.state in ['outcar_or_vasp_out_not_found', 'interrupted_writing_chgcar_or_wavecar']) or restart_with_vasp_error:
                path_dir_backup = backup(self.path_dir_run)
                logger.info('backup: %s' % (os.path.basename(path_dir_backup)))
                
                cp_r_atomic(self.path_dir_input, self.path_dir_run)
            
            if self.state == 'not_converged':
                path_dir_backup = backup(self.path_dir_run)
                logger.info('backup: %s' % (os.path.basename(path_dir_backup)))
                
                # ensure atomicity
                path_dir_run_tmp = get_tmp_path(self.path_dir_run)
                rm_fr_atomic(path_dir_run_tmp)
                cp_r_atomic(self.path_dir_input, path_dir_run_tmp)
                cp_r_atomic(join(path_dir_backup, 'INCAR'), join(path_dir_run_tmp, 'INCAR'))
                os.rename(path_dir_run_tmp, self.path_dir_run)
                
                incar = INCAR()
                incar.read_from_file(join(self.path_dir_run, 'INCAR'))
                nelm = int(incar.get_value('NELM'))
                new_nelm = int(nelm*self.nelm_scaling_factor)
                incar.set_value('NELM', new_nelm)
                incar.write(join(self.path_dir_run, 'INCAR'))
                logger.info('nelm: %d, new_nelm: %d' % (nelm, new_nelm))
            
            os.chdir(self.path_dir_run)
            
            logger.info('VASP start ...')
            start_time = time.time()
            self.run_vasp_func[self.server][self.vasp_version]()
            end_time = time.time()
            logger.info('VASP runtime: %d s' % (end_time-start_time))
            
            counter += 1
            self.check()
        
        if (counter==(self.max_time+1)) and (self.state!='finished'):
            logger.info('max_time: %d, final state: %s' % (self.max_time, self.state))
            raise MaxTimeExceededError(
                'VASPScf.run: max_time: %d' % (self.max_time)
            )
        
        logger.info('final state: %s' % (self.state))
