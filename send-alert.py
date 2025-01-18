import pywhatkit as pwk
 
# using Exception Handling to avoid unexpected errors
try:
     #pwk.sendwhatmsg_instantly("+12016732921", "hello", 15, True, 4)
     pwk.sendwhatmsg_to_group_instantly("JsiMLxfrPibAvzPECPQgdi", "Vengaboys trading bot calling Nullon.", 15, True, 4)
 
     print("Message Sent!") #Prints success message in console
 
     # error message
except: 
     print("Error in sending the message")