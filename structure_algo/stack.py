class Stack:
    def __init__(self):
        self.lst = []

    def lint(self,text):
        self.lst =[]
        for i in text:
            if self.open_brace(i):
                self.lst.append(i)
            elif self.close_brace(i):
                if self._empty():
                    return f"{text} doesn't have opening brace"

                pop_brace = self.lst.pop()
                
                if not self.mismatching(pop_brace,i):
                    return f"{text} has mismatched opening brace"
                
        if not self._empty():
            return f"{text} doesn't have closing brace"
        
        return f"{text} has matched brace"

    def _empty(self):
        if len(self.lst) == 0:
            return True
        else :
            return False
        
    @staticmethod
    def open_brace(open_text):
        if open_text in ['(','[','{']:
            return True
        
    @staticmethod
    def close_brace(closed_text):
        if closed_text in [')',']','}'] :
            return True
    @staticmethod
    def mismatching(open_text,closed_text):
        if open_text =='(' and closed_text == ')':
            return True
        elif open_text =='{' and closed_text == '}':
            return True
        elif open_text =='[' and closed_text == ']':
            return True
        else:
            return False

brace1 = Stack()
brace2 = Stack()
print(brace1.lint("([()])"))
print(brace2.lint(")))))"))