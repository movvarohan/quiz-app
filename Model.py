
# This class has all the information about one question.
# It is used to display the information on the question page to the user.
class Item:
    _qn = ""
    _incorrectanswer1 = ""
    _incorrectanswer2 = ""
    _incorrectanswer3 = ""
    _incorrectanswer4 = ""
    _correctanswer = ""
    _correctOption = ""
    _category = ""
    _level = ""

    # Constructor method to load all the information.
    def __init__(self, qn, incorrectanswer1, incorrectanswer2, incorrectanswer3,
                 incorrectanswer4, correctanswer, correctOption, category, level):
        self._qn = qn
        self._incorrectanswer1 = incorrectanswer1
        self._incorrectanswer2 = incorrectanswer2
        self._incorrectanswer3 = incorrectanswer3
        self._incorrectanswer4 = incorrectanswer4
        self._correctanswer = correctanswer
        self._correctOption = correctOption
        self._category = category
        self._level = level

    @property
    def qn(self):
        return self._qn
    @property
    def incorrectanswer1(self):
        return self._incorrectanswer1
    @property
    def incorrectanswer2(self):
        return self._incorrectanswer2
    @property
    def incorrectanswer3(self):
        return self._incorrectanswer3
    @property
    def incorrectanswer4(self):
        return self._incorrectanswer4
    @property
    def correctanswer(self):
        return self._correctanswer
    @property
    def correctoption(self):
        return self._correctOption
    @property
    def category(self):
        return self._category
    @property
    def level(self):
        return self._level

    # This is used for any debug purpose to write the question.
    def __str__(self):
        return self.qn
