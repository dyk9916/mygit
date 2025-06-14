# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 부모 디렉터리의 파일을 가져올 수 있도록 설정
import numpy as np
from common.optimizer import *

class Trainer:
    """신경망 훈련을 대신 해주는 클래스
    """
    # 객체 생성 시, network, x_train, t_train, x_test, t_test, epochs, mini_batch_size, optimizer, optimizer_param, evaluate_sample_num_per_epoch, verbose를 받음
    # network는 신경망 모델, x_train은 train data, t_train은 train data의 정답 레이블, x_test는 test data, t_test는 test data의 정답 레이블
    def __init__(self, network, x_train, t_train, x_test, t_test,
                 epochs=20, mini_batch_size=100,
                 optimizer='SGD', optimizer_param={'lr':0.01}, 
                 evaluate_sample_num_per_epoch=None, verbose=True):
        self.network = network
        self.verbose = verbose
        self.x_train = x_train
        self.t_train = t_train
        self.x_test = x_test
        self.t_test = t_test
        self.epochs = epochs
        self.batch_size = mini_batch_size
        self.evaluate_sample_num_per_epoch = evaluate_sample_num_per_epoch

        # optimzer
        optimizer_class_dict = {'sgd':SGD, 'momentum':Momentum, 'nesterov':Nesterov,
                                'adagrad':AdaGrad, 'rmsprpo':RMSprop, 'adam':Adam}
        self.optimizer = optimizer_class_dict[optimizer.lower()](**optimizer_param)
        
        self.train_size = x_train.shape[0]
        self.iter_per_epoch = max(self.train_size / mini_batch_size, 1)
        self.max_iter = int(epochs * self.iter_per_epoch)
        self.current_iter = 0
        self.current_epoch = 0
        
        self.train_loss_list = []
        self.train_acc_list = []
        self.test_acc_list = []

    def train_step(self):
        # train data에서 미니 배치를 뽑아냄
        batch_mask = np.random.choice(self.train_size, self.batch_size) # train data에서 batch_size만큼 랜덤하게 뽑아냄
        x_batch = self.x_train[batch_mask] # x_train에서 batch_mask에 해당하는 데이터를 뽑아냄
        t_batch = self.t_train[batch_mask] # t_train(정답 레이블블)에서 batch_mask에 해당하는 데이터를 뽑아냄
        
        # 미니 배치 사이즈 만큼의 데이터를 뽑아서 gradient를 구하고, optimizer를 활용해 params를 업데이트
        grads = self.network.gradient(x_batch, t_batch)   # 각 계층에서의 가중치, 편향에 대한 gradient를 구함
        self.optimizer.update(self.network.params, grads) # grads를 넘겨줌으로써 Optimizer를 활용해 params를 업데이트
        
        # 학습, 가중치 갱신 후의 loss를 구함
        loss = self.network.loss(x_batch, t_batch) # x_batch, t_batch를 넘겨줌으로써 loss를 구함
        self.train_loss_list.append(loss)
        if self.verbose: print("train loss:" + str(loss))
        
        if self.current_iter % self.iter_per_epoch == 0:
            self.current_epoch += 1
            
            # evaluate_sample_num_per_epoch가 None이면, 전체 train data와 test data에 대한 정확도를 구함
            x_train_sample, t_train_sample = self.x_train, self.t_train
            x_test_sample, t_test_sample = self.x_test, self.t_test
            # evaluate_sample_num_per_epoch가 None이 아닌 경우, evaluate_sample_num_per_epoch만큼의 데이터로 정확도를 평가
            if not self.evaluate_sample_num_per_epoch is None:
                t = self.evaluate_sample_num_per_epoch
                x_train_sample, t_train_sample = self.x_train[:t], self.t_train[:t]
                x_test_sample, t_test_sample = self.x_test[:t], self.t_test[:t]
            
            # 정확도 평가 
            # t개 만큼의 train data와 test data에 대한 정확도를 구함
            train_acc = self.network.accuracy(x_train_sample, t_train_sample)
            test_acc = self.network.accuracy(x_test_sample, t_test_sample)
            self.train_acc_list.append(train_acc)
            self.test_acc_list.append(test_acc)

            if self.verbose: print("=== epoch:" + str(self.current_epoch) + ", train acc:" + str(train_acc) + ", test acc:" + str(test_acc) + " ===")
        self.current_iter += 1
        
    # train시 train_step 함수 호출
    def train(self):
        for i in range(self.max_iter):
            # train_step() 함수에서는 train_acc, test_acc를 구하고, loss를 구함
            self.train_step()

        # 전체 test data의 정확도
        test_acc = self.network.accuracy(self.x_test, self.t_test)

        if self.verbose:
            print("=============== Final Test Accuracy ===============")
            print("test acc:" + str(test_acc))

