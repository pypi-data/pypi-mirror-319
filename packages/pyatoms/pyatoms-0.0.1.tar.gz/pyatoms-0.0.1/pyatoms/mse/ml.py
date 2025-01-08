class AMLInput:
    CLASSIFIER = [
        'adaboost', 
        'bernoulli_nb', 
        'decision_tree', 
        'extra_trees', 
        'gaussian_nb', 
        'gradient_boosting', 
        'k_nearest_neighbors', 
        'lda', 
        'liblinear_svc', 
        'libsvm_svc', 
        'mlp', 
        'multinomial_nb', 
        'passive_aggressive', 
        'qda', 
        'random_forest', 
        'sgd', 
    ]
    REGRESSOR = [
        'adaboost', 
        'ard_regression', 
        'decision_tree', 
        'extra_trees', 
        'gaussian_process', 
        'gradient_boosting', 
        'k_nearest_neighbors', 
        'liblinear_svr', 
        'libsvm_svr', 
        'mlp', 
        'random_forest', 
        'sgd', 
    ]
    
    def __init__(self):
        self.task_type = None
        
        self.dataset_name = None
        
        self.path_csv = None
        
        self.name_tag = None
        self.boolean = None
        self.categorical = None
        self.numerical = None
        
        self.label = None
        self.feature = None
        
        self.number_sample = None
        self.used_sample_index_0 = None
        
        self.estimator = None
        
        self.running_time = None
        self.per_run_time_limit = 3600
        self.memory_limit = 1024 * 8
        self.resampling_strategy = ['cv', 5]
        self.n_jobs = None
        
        self.test_size = 1/4
        self.metric_precision = 4
    
    def set_task_type(self, task_type):
        if task_type not in ['regression', 'classification']:
            raise Exception("materials_science_utils.AMLInput.set_task_type: task_type not in ['regression', 'classification']. task_type=%s" % (task_type))
        
        self.task_type = task_type
    
    def set_dataset_name(self, dataset_name):
        self.dataset_name = dataset_name
    
    def set_path_csv(self, path_csv):
        self.path_csv = path_csv
    
    def set_name_tag(self, name_tag):
        self.name_tag = name_tag
    
    def set_boolean(self, boolean):
        if self.name_tag == None:
            raise Exception("materials_science_utils.AMLInput.set_boolean: self.name_tag == None. Please set name_tag first.")
        
        for i in boolean:
            if i not in self.name_tag:
                raise Exception("materials_science_utils.AMLInput.set_boolean: i not in self.name_tag (for i in boolean). i=%s" % (i))
        
        self.boolean = boolean
    
    def set_categorical(self, categorical):
        if self.name_tag == None:
            raise Exception("materials_science_utils.AMLInput.set_categorical: self.name_tag == None. Please set name_tag first.")
        
        for i in categorical:
            if i not in self.name_tag:
                raise Exception("materials_science_utils.AMLInput.set_categorical: i not in self.name_tag (for i in categorical). i=%s" % (i))
        
        self.categorical = categorical
    
    def set_numerical(self, numerical):
        if self.name_tag == None:
            raise Exception("materials_science_utils.AMLInput.set_numerical: self.name_tag == None. Please set name_tag first.")
        
        for i in numerical:
            if i not in self.name_tag:
                raise Exception("materials_science_utils.AMLInput.set_numerical: i not in self.name_tag (for i in numerical). i=%s" % (i))
        
        self.numerical = numerical
    
    def set_label(self, label):
        boolean = [] if (self.boolean==None) else self.boolean
        categorical = [] if (self.categorical==None) else self.categorical
        numerical = [] if (self.numerical==None) else self.numerical
        
        if (label not in boolean) and (label not in categorical) and (label not in numerical):
            raise Exception("materials_science_utils.AMLInput.set_label: (label not in boolean) and (label not in categorical) and (label not in numerical). label=%s" % (label))
        
        self.label = label
    
    def set_feature(self, feature):
        boolean = [] if (self.boolean==None) else self.boolean
        categorical = [] if (self.categorical==None) else self.categorical
        numerical = [] if (self.numerical==None) else self.numerical
        
        for i in feature:
            if (i not in boolean) and (i not in categorical) and (i not in numerical):
                raise Exception("materials_science_utils.AMLInput.set_feature: (i not in boolean) and (i not in categorical) and (i not in numerical) (for i in feature). i=%s" % (i))
        
        self.feature = feature
    
    def set_number_sample(self, number_sample):
        self.number_sample = number_sample
    
    def set_used_sample_index_0(self, used_sample_index_0):
        if self.number_sample == None:
            raise Exception("materials_science_utils.AMLInput.set_used_sample_index_0: self.number_sample == None. Please set number_sample first.")
        
        for i in used_sample_index_0:
            if i not in range(self.number_sample):
                raise Exception("materials_science_utils.AMLInput.set_used_sample_index_0: i not in range(self.number_sample) (for i in used_sample_index_0)")
        
        self.used_sample_index_0 = used_sample_index_0
    
    def set_estimator(self, estimator):
        if self.task_type == None:
            raise Exception("materials_science_utils.AMLInput.set_estimator: self.task_type == None. Please set task_type first.")
        
        if estimator != 'all':
            if self.task_type == 'regression':
                for i in estimator:
                    if i not in self.REGRESSOR:
                        raise Exception("materials_science_utils.AMLInput.set_estimator: i not in self.REGRESSOR (for i in estimator). i=%s" % (i))
            
            if self.task_type == 'classification':
                for i in estimator:
                    if i not in self.CLASSIFIER:
                        raise Exception("materials_science_utils.AMLInput.set_estimator: i not in self.CLASSIFIER (for i in estimator). i=%s" % (i))
        
            self.estimator = estimator
        else:
            self.estimator = self.REGRESSOR if (self.task_type=='regression') else self.CLASSIFIER
    
    def set_running_time(self, running_time):
        self.running_time = running_time
    
    def set_per_run_time_limit(self, per_run_time_limit):
        self.per_run_time_limit = per_run_time_limit
    
    def set_memory_limit(self, memory_limit):
        self.memory_limit = memory_limit
    
    def set_resampling_strategy(self, resampling_strategy):
        self.resampling_strategy = resampling_strategy
    
    def set_n_jobs(self, n_jobs):
        self.n_jobs = n_jobs
    
    def set_test_size(self, test_size):
        self.test_size = test_size
    
    def set_metric_precision(self, metric_precision):
        self.metric_precision = metric_precision
    
    def write(self, path_saving):
        with open(path_saving, mode='w') as f:
            f.write('# Task type (regression or classification)\n')
            f.write('%s\n' % (self.task_type))
            f.write('# --------------------------------------------------\n')
            f.write('# Dataset name (used for display in AutoSklearn)\n')
            f.write('%s\n' % (self.dataset_name))
            f.write('# --------------------------------------------------\n')
            f.write('# Path csv\n')
            f.write('%s\n' % (self.path_csv))
            f.write('# --------------------------------------------------\n')
            f.write('# Name tag\n')
            for i in self.name_tag:
                f.write('%s ' % (i))
            f.write('\n')
            f.write('# Boolean (should be in "Name tag")\n')
            if self.boolean != None:
                for i in self.boolean:
                    f.write('%s ' % (i))
            f.write('\n')
            f.write('# Categorical (should be in "Name tag")\n')
            if self.categorical != None:
                for i in self.categorical:
                    f.write('%s ' % (i))
            f.write('\n')
            f.write('# Numerical (should be in "Name tag")\n')
            if self.numerical != None:
                for i in self.numerical:
                    f.write('%s ' % (i))
            f.write('\n')
            f.write('# --------------------------------------------------\n')
            f.write('# Label (should be in "Name tag")\n')
            f.write('%s\n' % (self.label))
            f.write('# Feature (should be in "Name tag")\n')
            for i in self.feature:
                f.write('%s ' % (i))
            f.write('\n')
            f.write('# --------------------------------------------------\n')
            f.write('# Number sample\n')
            f.write('%d\n' % (self.number_sample))
            f.write('# Used sample index (starting from 0)\n')
            for i in self.used_sample_index_0:
                f.write('%d ' % (i))
            f.write('\n')
            f.write('# --------------------------------------------------\n')
            f.write('# Estimator\n')
            for i in self.estimator:
                f.write('%s ' % (i))
            f.write('\n')
            f.write('# --------------------------------------------------\n')
            f.write('# Running time (s)\n')
            f.write('%d\n' % (self.running_time))
            f.write('# Per run time limit (s)\n')
            f.write('%d\n' % (self.per_run_time_limit))
            f.write('# Memory limit (MB)\n')
            f.write('%d\n' % (self.memory_limit))
            f.write('# Resampling strategy\n')
            for i in self.resampling_strategy:
                f.write('%s ' % (i))
            f.write('\n')
            f.write('# N jobs\n')
            f.write('%d\n' % (self.n_jobs))
            f.write('# --------------------------------------------------\n')
            f.write('# Test size\n')
            f.write('%f\n' % (self.test_size))
            f.write('# Metric precision\n')
            f.write('%d\n' % (self.metric_precision))
    
    def read(self, path):
        with open(path) as f:
            f.readline()
            self.set_task_type(f.readline().strip())
            f.readline()
            f.readline()
            self.set_dataset_name(f.readline().strip())
            f.readline()
            f.readline()
            self.set_path_csv(f.readline().strip())
            f.readline()
            f.readline()
            self.set_name_tag(f.readline().strip().split())
            f.readline()
            self.set_boolean(f.readline().strip().split())
            f.readline()
            self.set_categorical(f.readline().strip().split())
            f.readline()
            self.set_numerical(f.readline().strip().split())
            f.readline()
            f.readline()
            self.set_label(f.readline().strip())
            f.readline()
            self.set_feature(f.readline().strip().split())
            f.readline()
            f.readline()
            self.set_number_sample(int(f.readline().strip()))
            f.readline()
            self.set_used_sample_index_0([int(i) for i in f.readline().strip().split()])
            f.readline()
            f.readline()
            self.set_estimator(f.readline().strip().split())
            f.readline()
            f.readline()
            self.set_running_time(int(f.readline().strip()))
            f.readline()
            self.set_per_run_time_limit(int(f.readline().strip()))
            f.readline()
            self.set_memory_limit(int(f.readline().strip()))
            f.readline()
            content = f.readline().strip().split()
            if content[0] == 'cv':
                content[1] = int(content[1])
            self.set_resampling_strategy(content)
            f.readline()
            self.set_n_jobs(int(f.readline().strip()))
            f.readline()
            f.readline()
            self.set_test_size(float(f.readline().strip()))
            f.readline()
            self.set_metric_precision(int(f.readline().strip()))
