################################################################################
################################## BLUEBOTTLE ##################################
################################################################################
#
#  Copyright 2012 - 2016 Adam Sierakowski, The Johns Hopkins University
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  Please contact the Johns Hopkins University to use Bluebottle for
#  commercial and/or for-profit applications.
################################################################################

import sys, os, glob
import h5py as h5

# Initialize the reader by passing the directory containing the CGNS files. This
# returns a list containing the rounded time values available for reading.
def init(basedir):
  global t_read
  global base

  base = basedir

  t_read = list()

  files = glob.glob(base + "/part-*.cgns")
  if(len(files) == 0):
    print("cannot find any part-*.cgns files in", base)
    sys.exit()
  else:
    for i in files:
      start = i.find("part-")
      t_read.append(i[start+5:-5])

  return sorted(t_read, key=float)

# Open a particular CGNS file using a time value in the list returned by init().
def open(time):
  global f

  infile = base + "/part-" + time + ".cgns"

  try:
    f = h5.File(infile, 'r')
  except OSError:
    print("file", infile, "does not exist")

def open2(time1, time2):
  global f
  global g

  infile1 = base + "/part-" + time1 + ".cgns"
  infile2 = base + "/part-" + time2 + ".cgns"

  try:
    f = h5.File(infile1, 'r')
  except OSError:
    print("file", infile1, "does not exist")
  try:
    g = h5.File(infile2, 'r')
  except OSError:
    print("file", infile2, "does not exist")

# Close a particular CGNS file.
def close():
  f.close()

# Read the time.
def read_time():
  t1 = f["/Base/Zone0/Etc/Time/ data"][0]
  try:
    t2 = g["/Base/Zone0/Etc/Time/ data"][0]
  except NameError:
    return t1
  else:
    return (t1,t2)

# Read the particle positions.
def read_part_position():
  x1 = f["/Base/Zone0/GridCoordinates/CoordinateX/ data"]
  y1 = f["/Base/Zone0/GridCoordinates/CoordinateY/ data"]
  z1 = f["/Base/Zone0/GridCoordinates/CoordinateZ/ data"]
  try:
    x2 = g["/Base/Zone0/GridCoordinates/CoordinateX/ data"]
    y2 = g["/Base/Zone0/GridCoordinates/CoordinateY/ data"]
    z2 = g["/Base/Zone0/GridCoordinates/CoordinateZ/ data"]
  except NameError:
    return (x1,y1,z1)
  else:
    return ((x1,y1,z1),(x2,y2,z2))

# Read the particle velocities.
def read_part_velocity():
  u1 = f["/Base/Zone0/Solution/VelocityX/ data"]
  v1 = f["/Base/Zone0/Solution/VelocityY/ data"]
  w1 = f["/Base/Zone0/Solution/VelocityZ/ data"]
  try:
    u2 = g["/Base/Zone0/Solution/VelocityX/ data"]
    v2 = g["/Base/Zone0/Solution/VelocityY/ data"]
    w2 = g["/Base/Zone0/Solution/VelocityZ/ data"]
  except NameError:
    return (u1,v1,w1)
  else:
    return ((u1,v1,w1),(u2,v2,w2))
