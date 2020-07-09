
class Complex:
	def __init__(self, num1, num2):
		self.num1=num1
		self.num2=num2
	def __str__(self):
		if self.num1==0:
			return("{:d}i".format(self.num2))
		elif self.num2<0:
			return("{:d}{:d}i".format(self.num1, self.num2))
		elif self.num2>0:
			return("{:d}+{:d}i".format(self.num1, self.num2))
		else:
			return("{:d}".format(self.num1))

