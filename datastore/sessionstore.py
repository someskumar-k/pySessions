import datetime
class SessionStore:
    def __init__(self):
        self.usersessionlist={}
        self.activesession={}
    
    def add(self,sid=None,usr_id=None,timeout=None):
        self.add_active_session(sid,usr_id,timeout)
        self.add_session_user(usr_id,sid)

    def get_session(self, sid):
        if sid in self.activesession :
             return self.activesession[sid]
        else :
            raise Exception
    def remove(self,sid):
        try:
            usr = self.activesession[sid].get("user")
            self.activesession.pop(sid)
            usrlist = self.usersessionlist.get(usr)
            usrlist.remove(sid);
            self.usersessionlist.update({usr:usrlist})
            return
        except Exception as exec :
            return 
   
    def get_sessionlist(self,uid):
        if uid == None :
            raise Exception("Invalid user id")
        if uid in self.usersessionlist :
            return self.usersessionlist[uid]
        raise Exception("No data found")

    def add_active_session(self,id,usr_id,time):
        self.activesession.update({id:{"user":usr_id,"time_ms":time}})
                
    def add_session_user(self,usr_id,id):
        if usr_id in self.usersessionlist :
            lst = self.usersessionlist[usr_id];
            lst.append(id)
            self.usersessionlist.update({usr_id:lst})
        else :
            lst=[]
            lst.append(id)
            self.usersessionlist.update({usr_id:lst})
