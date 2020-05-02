import hashlib
import datetime

from .datastore import  sessionstore;
class Authenticator:
    @staticmethod
    def module_info():
        return {
            'version':'v1.0.0',
            'buildnumber':'1000',
            'description':'User session handling module on python.',
            'license':'GNU General Public License v3.0',
            'author':'SOMES KUMAR K'
            }

    def __init__(self,unique_key=None,timeout=10000,demo=False):
        if(unique_key == None):
            raise Exception("No unique key is present")
        if timeout == None or timeout<=5000 :
            raise Exception("Minimum time is 5000")
        self.appkey = unique_key
        self.default_timeout = timeout
        self.store = sessionstore.SessionStore();
        self.isdemo = demo;

    def manage(self,user_id=None,time_limit=None):
        return_data = {}
        if self.isdemo :
            return_data.update({"info" :self.module_info()})
        try :
            if user_id == None : 
                raise Exception("Illeagal Argument")
            if time_limit == None or time_limit<=5000 :
                time_limit = self.default_timeout
            timeout = datetime.datetime.utcnow().replace(microsecond=0)
            timeout=int(timeout.strftime("%s"))+time_limit
            ustr = user_id+"_"+self.appkey+"_"+str(timeout)+""
            ustr = hashlib.md5(ustr.encode()).hexdigest()
            self.store.add(ustr,user_id,timeout)
            return_data.update({"session_id" :ustr,"status" : "success","timeout":timeout});
            return return_data
        except Exception as exec:
            return_data.update({"status":"failed","message":"Error Occured"})
            return return_data

    def validate(self,session_id=None):
        return_data = {}
        if self.isdemo :
            return_data.update({"info" :self.module_info()})
        try:
            if session_id == None :
                raise Exception("No parameter found")
            sessiondta =  self.store.get_session(session_id)
            timeout = sessiondta.get("time_ms")
            cur_time = datetime.datetime.utcnow().replace(microsecond=0)
            cur_time=int(cur_time.strftime("%s"))
            if cur_time<=timeout :
                self.store.remove(session_id)
                return_data.update({"status" : "success","valid":True})
                return return_data
            else :
                return_data.update({"status" : "success","valid":False})
                return return_data
        except Exception as exec :
            return_data.update({"status" : "failure","message":"Error Occured","valid":False})
            return return_data

    def active_sessions(self,uid):
        return_data = {}
        if self.isdemo :
                return_data.update({"info" :self.module_info()})
        return_data.update({"user_id":uid})
        try:
            
            if uid == None :
                raise Exception("No data is given")
            sesList = self.store.get_sessionlist(uid)
            sesarr =[] 
            for ses in sesList :
                sess = self.store.get_session(ses);
                sess.update({"session_id":ses})
                sesarr.append(sess)
            return_data.update({"active_sessions":sesarr,"status":"success"})
            return return_data
        except Exception as exec :
            return_data.update({"status" : "failure","message":"Error Occured"})
            return return_data

    def block(self,session_id):
        return_data = {}
        if self.isdemo :
            return_data.update({"info" :self.module_info()})
        self.store.remove(session_id)
        return_data.update({"status" : "success"})
        return return_data