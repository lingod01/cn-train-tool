from piston.emitters import Emitter

from train.provider._12306 import format_trains
class TextTableEmitter(Emitter):
    #TODO 
    def render(self, request):
        return format_trains(self.construct(), 'text')

class HtmlEmitter(Emitter):
    #TODO 
    def render(self, request):
        return format_trains(self.construct(), 'html')



