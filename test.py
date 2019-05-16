# -*- coding: utf-8 -*-
import ipfsapi
from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from ipfs_model import hashid
from ipfs_model import db
from ipfs_model import app
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_wtf import Form
import uuid

api = ipfsapi.connect('129.211.27.244', 5001)
