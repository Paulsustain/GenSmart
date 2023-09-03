import sys
sys.path.append('/home/pi/smarteye/crons')
sys.path.append('/home/pi/smarteye/db')
import jobs as cron_jobs
import migrations

def rerun_jobs_at_reboot():
    cron_jobs.main()

def rerun_migrations_at_reboot():
    migrations.run_migrations()


def main():
    rerun_jobs_at_reboot()
    rerun_migrations_at_reboot()

if __name__=="__main__":
    main()