#!/bin/bash
export FLASK_APP=/mote_server/m_web_mote.py && flask run --host=0.0.0.0 --port=5005 >> /mote_server/mote.log 2> /mote_server/mote_error.log
