##################################################
##################################################
"""               NGUYEN CONG HUY              """
####    ##################   #####    ####    ####
####    ##################   ######   ####    ####
####          ######         #### ##  ####    ####
####          ######         ####  ## ####    ####
####          ######         ####   ######    ####
####          ######         ####   ######    ####
####                TOFU NGUYEN               ####
##################################################
##################################################

###########################################################################
#### Module's name: Date and Time handling                             ####
#### Programmer: Nguyen Cong Huy (Nickname: Tofu Nguyen)               ####
#### Finished date: Sunday, December 29, 2024                          ####
###########################################################################

# Importing necessary libraries
import datetime
import time

class DateTime:
	# Getting current time
	def currentTime(self):
		t = time.localtime()
		current_time = time.strftime("%H:%M:%S", t)
		return current_time

	# Getting current date
	def currentDate(self):
		now = datetime.datetime.now()
		day = now.strftime('%A')
		date = str(now)[8:10]
		month = now.strftime('%m')
		year = str(now.year)
		
		# Converting to Vietnamese
		if day == "Sunday":
			day = "Chủ Nhật"
		elif day == "Monday":
			day = "Thứ Hai"
		elif day == "Tuesday":
			day = "Thứ Ba"
		elif day == "Wednesday":
			day = "Thứ Tư"
		elif day == "Thursday":
			day = "Thứ Năm"
		elif day == "Friday":
			day = "Thứ Sáu"
		elif day == "Saturday":
			day = "Thứ Bảy"

		result = f'{day}, ngày {date} tháng {month}, {year}'
		return result

###########################################################################
####                                                                   ####
####                © 2024 Mary Assistant | Tofu Nguyen                ####
####                                                                   ####
###########################################################################