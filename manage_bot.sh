#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

case "$1" in
    start)
        echo "Starting traffic bot..."
        cd "$SCRIPT_DIR"
        python3 traffic_bot.py &
        echo $! > bot.pid
        ;;
    stop)
        echo "Stopping traffic bot..."
        if [ -f bot.pid ]; then
            kill $(cat bot.pid)
            rm bot.pid
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    status)
        if [ -f bot.pid ]; then
            if ps -p $(cat bot.pid) > /dev/null; then
                echo "Traffic bot is running (PID: $(cat bot.pid))"
            else
                echo "Traffic bot is not running (PID file exists but process is dead)"
                rm bot.pid
            fi
        else
            echo "Traffic bot is not running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0 