Contains:
	-> AudioServer.py
	-> Requirements.txt
	-> audio.db
---------
Works on python3 with modules on Requirements.txt and sqllite installed

---------
Supports following HTTPS methods:
		->Get  -To Fetch record based on ID  -------->returns 200 on sucuess , 400 on fail
		->Post -To create a record for a particualr ID -------->returns 200 on sucuess , 400 on fail
		->Put  -To Update a record for particualr ID -------->returns 200 on sucuess , 400 on fail
		->Delete -To delete a record based on ID -------->returns 200 on sucuess , 400 on fail
		

****************Uploaded_time Format must be in following datetime format.********************
							%m/%d/%y %H:%M:%S sample 12/20/95 12:30:00