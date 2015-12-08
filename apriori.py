# -*- coding:utf-8 -*-

def main():
    #テスト用main
    item_list = ['https://github.com/ygd-project/a', 'https://github.com/ygd-project/b','https://github.com/ygd-project/c']
    tran_list = [['https://github.com/ygd-project/a', 'https://github.com/ygd-project/b'], ['https://github.com/ygd-project/a'],['https://github.com/ygd-project/a','https://github.com/ygd-project/c']]
    a = Apriori(item_list, tran_list)
    s = a.go_analyze()
    print(s)
    
class Apriori:
    MIN_SUPPORT = 0.1
    MAX_DEPTH = 4
    def __init__(self, item_list, tran_list):
        self.item_list = item_list
        self.tran_list = tran_list
        self.item_sel_list =[[item] for item in item_list]
        self.tran_num = len(tran_list)
        self.relation_dict = {}
        self.support_list = []
        
        #一応動的に決定してみる
        #self.MIN_SUPPORT = ( self.MAX_DEPTH - 1.0 ) / self.tran_num
        
    def go_analyze(self):
        self.relation_dict = self.create_relation(self.item_list, self.tran_list, self.tran_num)
        self.support_list = self.calc_combination(self.relation_dict, self.tran_num, self.item_sel_list, self.MIN_SUPPORT, self.MAX_DEPTH)
        return self.support_list
    def create_relation(self, item_list, tran_list, tran_num):
        #関連性を導出
        relation_dict = {}
        for item in item_list:
            for n in range(tran_num):
                if item in self.tran_list[n]:
                    if relation_dict.has_key(item):
                        relation_dict[item].append(n)
                    else:
                        relation_dict[item] = [n]
        return relation_dict
    
    def calc_combination(self, relation_dict, tran_num, item_sel_list, min_support, max_depth):
        support_list = []
        depth = 1
        
        #指定の深さまでループする
        while item_sel_list != []:
            current_depth_item_list = []
            for item_sel in item_sel_list:
                relation_check_num = self.calc_support(tran_num, relation_dict, item_sel)
                support = 1.0 * relation_check_num / tran_num
                if support >= min_support:
                    support_list.append([item_sel, support])
                    current_depth_item_list.append(item_sel)
                    
            #最初の階層の組み合わせを記憶する
            if depth == 1:
                first_depth_item_list = current_depth_item_list[:]
            #最深部でブレークする
            if max_depth <= depth:
                break
            item_sel_list = self.create_combination(current_depth_item_list, first_depth_item_list)
            depth += 1
            
        return support_list
            
    def calc_support(self, tran_num, relation_dict, item_sel):
        relation_check_set = set(range(tran_num))
        
        #アイテム全てがリレーションのキーにあるかチェックする
        for item in item_sel:
            if item in relation_dict:
                relation_check_set = relation_check_set.intersection(set(relation_dict[item]))
        relation_check_num = len(relation_check_set)
        return relation_check_num
    
    def create_combination(self, current_item_list, first_item_list):        
        #カレントをファーストを比較して、アイテム絞られていればカレントを利用する
        #そうでない(増えた場合)は余分な組み合わせがあるのでファーストを利用する
        if len(current_item_list) < len(first_item_list):
            add_base_list = current_item_list
        else:
            add_base_list = first_item_list
            
        combination_list = []
            
        for item in current_item_list:
            for add in add_base_list:
                item_num = len(item)
                added_item = set(item).union(set(add))
                added_item_num = len(added_item)
                if ((item_num + 1) == added_item_num) and (added_item not in combination_list):
                    combination_list.append(added_item)
                    
        combination_sel_list =[list(item) for item in combination_list]
        return combination_sel_list
                    
    
if __name__ == '__main__':
    main()
