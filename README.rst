MocaNexion: Connect to MOCA with Python
===================

Installation:

    pip install mocanexion

Usage:

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
    
    
    
Notes:

    device, warehouse, locale are optional arguments for connect() method and will set environment variables if passed in
    

