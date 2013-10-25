#!/usr/bin/env python
import os
import time
import shutil
import dopy.manager

class PondManager(object):

    def __init__(self, client_id, api_key):
        self.client_id = client_id
        self.api_key = api_key

    def location(self, pond):
        return pond['pond_dir'] + '/' + pond['pond_name']

    def hosts_path(self, pond):
        return self.location(pond) +  '/.pond'

    def fill(self, pond):

        if not os.path.exists(self.location(pond)):
            os.makedirs(self.location(pond))

        open(self.hosts_path(pond), 'a').close()

        for droplet in pond['droplets']:
            for i in range(droplet['num']):
                if os.path.getsize(self.hosts_path(pond)) == 0:
                    pond_hosts = {}
                else:
                    with open(self.hosts_path(pond), 'r') as pond_hosts_file:
                        pond_hosts = json.load(pond_hosts_file)

                ip_address, id = self.__create_droplet(pond['pond_name'], droplet['config'])
                pond_hosts[ip_address] = id

                with open(self.hosts_path(pond), 'w') as pond_hosts_file:
                    json.dump(pond_hosts, pond_hosts_file)

    def __create_droplet(self, pond_name, droplet):

        do = dopy.manager.DoManager(self.client_id, self.api_key)

        droplet_name = pond_name + '--' + droplet['name']
        create_response = do.new_droplet(droplet_name, droplet['size_id'], droplet['image_id'], droplet['region_id'], droplet['ssh_key_ids'])

        event_id = create_response['event_id']
        id = create_response['id']

        event_response = do.show_event(event_id)
        while (event_response['action_status'] != "done"):
            time.sleep(5)
            event_response = do.show_event(event_id)

        droplet_response = do.show_droplet(id)

        print("created droplet: " + str(droplet_response))

        return (droplet_response['ip_address'], droplet_response['id'])
		
    def drain(self, pond):

        if os.path.exists(self.hosts_path(pond)) and os.path.getsize(self.hosts_path(pond)) != 0:

            with open(self.hosts_path(pond), 'r') as pond_hosts_file:
                pond_hosts = json.load(pond_hosts_file)

            do = dopy.manager.DoManager(self.client_id, self.api_key)
            for ip_address in pond_hosts:
               do.destroy_droplet(pond_hosts[ip_address])
               print("destroyed droplet: " + str(pond_hosts[ip_address]) + " with ip: " + ip_address)

        shutil.rmtree(self.location(pond), True)

if __name__=='__main__':
    import sys
    import json

    usage = "Usage: pond.py pond (fill|drain|refill)"

    if not 'DO_CLIENT_ID' in os.environ:
        print "DO_CLIENT_ID is not set"
        sys.exit(1)

    if not 'DO_API_KEY' in os.environ:
        print "DO_API_KEY is not set"
        sys.exit(1)

    client_id = os.environ['DO_CLIENT_ID']
    api_key = os.environ['DO_API_KEY']

    if len(sys.argv) != 3:
       print usage
       sys.exit(1)

    with open(sys.argv[1]) as pond_file:
        pond = json.load(pond_file)

    if not 'pond_dir' in pond:
        pond['pond_dir'] = os.path.expanduser("~") + '/.ponds'

    pm = PondManager(client_id, api_key)

    action = sys.argv[2]
    if action == "fill":
        pm.fill(pond)
    elif action == "drain":
        pm.drain(pond)
    elif action == "refill":
        pm.drain(pond)
        pm.fill(pond)
    else:
        print usage
        sys.exit(1)
                               