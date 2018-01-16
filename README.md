
MocaNexion
======

**Connect to MOCA with Python!**

To Install::

    pip install mocanexion

Introduction
____________

MocaNexion allows you to connect to a MOCA application server using your application credentials.  
Once authenticated, you can then run MOCA commands and have the results returned back to you in a 
Pandas dataframe.

Usage
____________

    >>>>from mocanexion import MocaNexion

    >>>>moca = MocaNexion()
    
    >>>>moca.connect(login_url, user_id, password, device=None, warehouse=None, locale=None)
    
    >>>>status, res = moca.execute("publish data where test = 'Success'")
    
    >>>>print(status)
    
    0
    
    >>>>print(res)
    
    test
    ----
    Success
    
    
    
Notes
____________

* Device, warehouse, and locale are optional arguments for the connect() method and will set environment variables if passed in
    
