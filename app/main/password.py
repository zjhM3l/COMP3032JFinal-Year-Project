class PasswordTool():
    """
    密码工具类
  """

    def __init__(self, password):
        self.password = password
        self.strength_level = 0

    def check_number_exist(self):
        """
      判断是否含数字
    """
        has_number = False
        for c in self.password:
            if c.isnumeric():
                has_number = True
                break
        return has_number

    def check_letter_exist(self):
        """
      判断是否含字母
    """
        has_upper_letter = False
        has_lower_letter = False
        for c in self.password:
            if c.isupper():
                has_upper_letter = True
            elif c.islower():
                has_lower_letter = True
            has_both_letter = has_upper_letter and has_lower_letter
            if has_both_letter:
                break
        return has_both_letter

    def check_specialchar_exist(self):
        """
      判断是否包含特殊字符
    """
        has_specialchar = False
        specialchar_list = ['+', '-', '*', '/', '_', '&', '%', ',']
        for c in self.password:
            if c in specialchar_list:
                has_specialchar = True
                break
        return has_specialchar

    def process_password(self):
        """
      判断是否符合规则
    """
        # 规则1：长度至少8位
        # if len(self.password) >= 8:
        #     self.strength_level += 1
        #
        # # 规则2：必须包含数字
        # if self.check_number_exist():
        #     self.strength_level += 1
        #
        # # 规则3：必须包含大小写字母
        # if self.check_letter_exist():
        #     self.strength_level += 1
        #
        # # 规则4：需要包含特殊字符
        # if self.check_specialchar_exist():
        #     self.strength_level += 1


