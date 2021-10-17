from DB.DBinit import DataBaseHandler, User, Server
import random


class UserDB:
    def __init__(self):
        pass
    
    def add_registered_user(self, msg, server, serv_id):
        tgid = msg.from_user.id
        discordid = msg.text
        try:
            try:
                DataBaseHandler.connect()
            except Exception as ex:
                print(ex)
            User.create_table()
            User.create(
                tg_user_id = tgid,
                ds_user_id = discordid,
                servers = server,
                server_id = serv_id
            )
        except Exception as ex:
            print(f"UserDB{ex}")
            return False
        finally:
            DataBaseHandler.close()
        return True
        
    def get_servers(self, id):
        try:
            try:
                DataBaseHandler.connect()
            except: pass
            servers = []
            for user in User.select():
                if str(user.tg_user_id) == str(id):
                    servers.append(user)
        except Exception as ex: 
            print(ex)
        finally:
            DataBaseHandler.close()
        try:
            return servers
        except:
            return []
        

class ServerDB:
    def __init__(self):
        pass
    
    def __keygen(self):
        try:
            try:
                DataBaseHandler.connect()
            except: pass
            Server.create_table()
            rand = lambda: random.randint(1000, 9999)
            keys = Server.select(Server.reg_key).distinct()
            key = rand()
            while key in keys:
                key = rand()
        except Exception as ex:
            print(ex)
        finally:
            DataBaseHandler.close()
        return key
            
    def reg(self, guild):
        name = guild.name
        id = guild.id
        reg_key = self.__keygen()
        try:
            try:
                DataBaseHandler.connect()
            except:
                pass
            Server.create_table()
            for serv in Server.select():
                if int(serv.server_id) == int(id):
                    print("INIF")
                    DataBaseHandler.close()
                    return
            Server.create(
                name=name,
                server_id=id,
                reg_key=reg_key
                )
        except Exception as ex:
            print(ex)
        finally:
            DataBaseHandler.close()
        
    def get_key(self, id):
        try:
            try:
                DataBaseHandler.connect()
            except: pass
            serv = Server.select(Server.reg_key).where(Server.server_id == id).get()
        except Exception as ex:
            print(ex)
        finally:
            DataBaseHandler.close()
        return int(serv.reg_key)
    
    def get_servers(self):
        try:
            try:
                DataBaseHandler.connect()
            except: pass
            servers = Server.select()
        except Exception as ex:
            print(ex)
        finally:
            DataBaseHandler.close()
        return servers
