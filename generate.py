import MeCab
import ipadic
import markovify

class markov:
    def __init__(self,txt):
        self.txt = txt
        self.lines = 'メロスは激怒した。'
        self.new_lines=''
    
    def wakachi(self):
        
        #txtファイルから文章を読み込む
        with open(self.txt,"r",encoding="utf-8") as f:
            words = f.readlines()
    
        words_list = []
        #改行で文章を区切る
        for i in words:
            word = i.split('\n')
            words_list.append(word)
            
        #形態素解析
        mecab = MeCab.Tagger(ipadic.MECAB_ARGS)

        # 上手く解釈できない文字列を定義しておく
        breaking_chars = ['(', ')', '[', ']', '"', "'"]
        # 最終的に1文に収めるための変数
        self.splitted_meigen = ''

        for line in words_list:
            # print('Line : ', line)
            # lineの文字列をパースする
            
            if(line != []):
            
                parsed_nodes = mecab.parseToNode(line[0])

                while parsed_nodes:
                    try:
                        # 上手く解釈できない文字列は飛ばす
                        if parsed_nodes.surface not in breaking_chars:
                            self.splitted_meigen += parsed_nodes.surface
                        # 句読点以外であればスペースを付与して分かち書きをする
                        if parsed_nodes.surface != '。' and parsed_nodes.surface != '、':
                            self.splitted_meigen += ' '
                        # 句点が出てきたら文章の終わりと判断して改行を付与する
                        if parsed_nodes.surface == '':
                            self.splitted_meigen += '\n'
                    except UnicodeDecodeError as error:
                        print('Error : ', line)
                    finally:
                        # 次の形態素に上書きする。なければNoneが入る
                        parsed_nodes = parsed_nodes.next

    def makelines(self):
        # マルコフ連鎖のモデルを作成
        model = markovify.NewlineText(self.splitted_meigen,state_size=2)
        
        sentence = model.make_sentence(tries=100)
        if sentence is not None:    
            self.lines += self.new_lines 
            self.new_lines = ''.join(sentence.split())
        else:
            self.new_lines=''

            
            
    def reset(self):
        self.lines = 'メロスは激怒した。'
        self.new_lines=''