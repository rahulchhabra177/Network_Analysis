#imports
from scapy.all import *
import matplotlib.pyplot as plt
import argparse

X_LIM = 25
Y_LIM = 100
MAX_HOPS = 100
COLOR  = "purple"
hops = []
Rtimes = []
table_text = [["Hop Count","Round Trip Time","Router IP Address"]]
def ping(ip , ttl_val , timeout):
    ping_packet = IP(dst = ip , ttl = ttl_val) / ICMP()
    reply = sr1(ping_packet , timeout = timeout)
    if reply is None:
        return ("*" , 0 , False)
    sending_time = ping_packet.sent_time
    receiving_time = reply.time
    time_elapsed = receiving_time - sending_time
    # print(reply.summary())
    sum  = reply.summary()
    if not "time-exceeded" in sum:
        return (reply.src ,time_elapsed , True)
    print(reply.show())
    return (reply.src , time_elapsed , False)

def convert_to_ms(t):
    t = t*1000
    t = round(t)
    return t

def update_x():
    global X_LIM
    X_LIM+=10
    plt.xlim(0,X_LIM)

def update_y(val):
    global Y_LIM
    Y_LIM = val + 10
    plt.ylim(0,Y_LIM)    

def initialise_plot(hostname):
    global X_LIM,Y_LIM
    plt.xlim(0,X_LIM)
    plt.ylim(0,Y_LIM)
    plt.subplots_adjust(right=0.55)
    plt.title("Plot of RTT vs Hop Count for " + hostname , color = "green")
    plt.xlabel("Hop Count" , color = "red")
    plt.ylabel("Round Trip Time (in milliseconds)" , color = "red")

def add_to_plot(x , y , router_addr):
    hops.append(x)
    Rtimes.append(y)
    plt.plot(hops, Rtimes , color = COLOR)
    table_text.append([str(x),str(y)+" ms" , router_addr])
    the_table = plt.table(cellText=table_text,
                      loc='right')
    plt.pause(0.2)

def traceroute(ip , max_hops, timeout):

    for ttl_val in range(1 , max_hops):
        router_addr , time_elapsed  , completed = ping(ip , ttl_val , timeout)
        time_f = convert_to_ms(time_elapsed)
        if ttl_val+1 >= X_LIM:
            update_x()
        if time_f +1 >= Y_LIM:
            update_y(time_f)

        print(str(time_f) + " ms" , router_addr)
        add_to_plot(ttl_val , time_f , router_addr)
        if completed:
            break

if __name__=="__main__":
    #for parsing command line arguments
    parser = argparse.ArgumentParser(description='Implementation of Traceroute command by using repeated pings with varying TTL value')
    parser.add_argument('--hostname', help='IP addresss or name of website you wish to find route', type=str, default="www.iitd.ac.in")
    parser.add_argument('--savefile', help='name of saved PNG image', type=str, default="plot")
    parser.add_argument('--hops', help='Specify the maximum number of hops', type=int, default=100)
    parser.add_argument('--timeout', help='Specify the timeout for request', type=int, default=10)
    args = parser.parse_args()
    #initialising plot with labels title etc.
    initialise_plot(args.hostname)	
    traceroute(args.hostname , args.hops , args.timeout)
    
    plt.savefig('./plots/'+ args.savefile +'.png', dpi=300, bbox_inches='tight')
    print("Plot Saved to ./plots/"+ args.savefile +".png")
