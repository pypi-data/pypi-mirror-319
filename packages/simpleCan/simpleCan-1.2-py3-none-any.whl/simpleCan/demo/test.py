import time
import simpleCan

simpleCan = simpleCan.SimpleCan()
excel_path = 'signal_table.xlsx'
simpleCan.update_Excel_path(excel_path)
simpleCan.env_run()
simpleCan.sendMessage(message_id = 0xCFE6CEE, data= [0, 0, 0, 0, 0, 0, 0x9A, 0x19], period=0.02, duration=20)
time.sleep(20)