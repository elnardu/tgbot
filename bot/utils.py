
def frmDuration(duration):
	hours = int(duration/60)
	minutes = duration - hours*60
	return "{}:{:02d}".format(hours, minutes)