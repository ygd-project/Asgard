# -*- coding:utf-8 -*-
from apriori import Apriori
import pickle
import sys
def main():
    if len(sys.argv) != 2:
        print("USAGE python main.py [load_data|load_target]")
        sys.exit()
    mode = sys.argv[1]
    if mode == "load_data":
        c = Control()
        c.proc_load()
    elif mode == "load_target":
        c = Control()
        c.proc_macth()
        c.view_support_list()

class Control:

    def __init__(self):
        self.csv_data_file = "data.csv"
        self.csv_target_file = "target.csv"
        self.pickle_file = "pickle.dump"
        self.tran_dict = {}
        self.key_list = []
        self.value_list = []
        self.tran_list = []

        self.target_list = []
        self.support_list = []

    def proc_load(self):
        self.load_data_csv()
        self.go_apriori()
        self.save_pickel()

    def proc_macth(self):
        self.load_pickel()
        self.load_target_csv()
        self.go_macth()

        return self.result_list

    def load_data_csv(self):
        key_set = set()
        value_set = set()

        f = open(self.csv_data_file, "r")

        for line in f:
            #CSV分解
            line_sp = line.split(",")
            #一列目をキー
            key = line_sp[0]
            #二列目をバリュー(改行削除)
            value = line_sp[1].strip("\n")

            #ユニークを取る
            key_set = key_set.union(set([key]))
            value_set = value_set.union(set([value]))

            #トランザクションデータに変換
            if self.tran_dict.has_key(key):
                self.tran_dict[key].append(value)
            else:
                self.tran_dict[key]=[value]
        f.close()

        #後処理
        #キーリスト
        self.key_list = list(key_set)
        #バリューリスト
        self.value_list = list(value_set)
        #トランザクションリスト
        self.tran_list = self.tran_dict.values()

    def go_apriori(self):
        a = Apriori(self.value_list, self.tran_list)
        self.support_list = a.go_analyze()

    def load_target_csv(self):
        f = open(self.csv_target_file, "r")

        for line in f:
            #改行削除
            value = line.strip("\n")
            self.target_list.append(value)
        f.close()

    def go_macth(self):
        key = self.target_list
        key_set = set(key)
        user_support_list = []

        #xを含むトランザクションを見つける
        for support in self.support_list:
            support_key = support[0]
            support_key_set = set(support_key)
            support_value = support[1]
            macth_key_set = support_key_set.intersection(key_set)
            #すべてのキーを持っている、かつ、キーの数とサポートのキーが同じ
            if (len(macth_key_set) == len(key_set))and (len(support_key_set) == len(key_set)):
                base_value = support_value

        #xかつyのトランザクションを見つける
        for support in self.support_list:
            support_key = support[0]
            support_key_set = set(support_key)
            support_value = support[1]
            macth_key_set = support_key_set.intersection(key_set)
            #すべてのキーを持っている、かつ、キーの数よりサポートのキーが多い(レコメンド対象)
            if (len(macth_key_set) == len(key_set))and (len(support_key_set) > len(key_set)):
                recommend_key = list(support_key_set.difference(key_set))
                recommend_key_set = set(recommend_key)
                confidence = support_value / base_value

                #yを含むトランザクションを見つける
                for sub_support in self.support_list:
                    sub_support_key = sub_support[0]
                    sub_support_key_set = set(sub_support_key)
                    sub_support_value = sub_support[1]
                    sub_macth_key_set = sub_support_key_set.intersection(recommend_key_set)

                    #すべてのキーを持っている、かつ、キーの数とサポートのキーが同じ
                    if (len(sub_macth_key_set) == len(recommend_key_set))and (len(sub_support_key_set) == len(recommend_key_set)):
                        sub_value = sub_support_value
                        lift = confidence / sub_value

                        user_support_list.append([recommend_key, lift, confidence, support_value])
                        break

        self.result_list = sorted(user_support_list, key=lambda x:x[1], reverse=True)

    def view_support_list(self):
        for line in self.result_list:
            print(line[0],line[1])

    def save_pickel(self):
        f = open(self.pickle_file, "w")
        pickle.dump(self.support_list, f)
        f.close()

    def load_pickel(self):
        f = open(self.pickle_file, "r")
        self.support_list = pickle.load(f)
        f.close()

if __name__ == '__main__':
    main()
