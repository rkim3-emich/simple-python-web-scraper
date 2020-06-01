import socket, ssl
import time
import html

WEB = "www.youtube.com"
PORT = 443

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssock = ssl_context.wrap_socket(s, server_hostname=WEB)
ssock.connect((WEB, 443))
ssock.send(("GET / HTTP/1.1\r\nHost: " + WEB + "\r\n\r\n").encode())
def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)
    
    #total data partwise in an array
    total_data=[];
    data='';
    
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
        
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
        
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
    
    #join all parts to make final string
    return ''.join(str(total_data))

#get reply and print
response = recv_timeout(ssock)
ssock.close
total = ""
for chunks in response:
    total += chunks

html_start = total.lower().find("<html")
html = html.unescape(total[html_start:len(total)])

if html_start >= 0:
    with open("test.html", "w") as writer:
        writer.write(html)
