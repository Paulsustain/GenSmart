import sys
sys.path.append('/home/pi/smarteye/data/probe')
import main_multicont

def get_mtc_data():
    try:
        main_multicont.query_probes()
    except:
        print("could not log mtc data to remote db")

def main():
    get_mtc_data()

if __name__ == '__main__':
    main()
