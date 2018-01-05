MocaNexion: Connect to MOCA with Python
===================

Installation:

    pip install mocanexion

Usage:

    from mocanexion import MocaNexion

    moca = MocaNexion()
    
    moca.connect(login_url, user_id, password)
    
    moca.execute(moca_command)

