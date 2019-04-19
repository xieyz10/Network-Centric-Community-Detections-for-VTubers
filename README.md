vtuberminer
======================================

This is a vtuber analysis project ~~~~

Hi every DD~~~

--------------------------------------

## Environment:
- Java 8(just because my friend only know java)
- python 3.5.6
- Linux 4.19
- mongodb

**For contributer:**

- update your twi account or google account meta info in meta.json, I will delete this after all finish, and mark this project as open
- plz use vscode editor for py repo, and IntelliJ for java repo
- plz make sure pylint and autopep8 is on, and follower it's code lint and name rule as possible, **just for convience of merge code.** any white list setting should be shared with us
- use maven not gradle for java user
- use npm not yarn for js dev
- it will be much easier if some one write a DockerFile especially when some one using tensorflow~~~ 

---------------------------------------

## File Structure

- `/python` : python source file
- `meta.json`: all configuration, Auth info.
- `/data`: folder for harvested data

---------------------------------------

Generally speaking, this project has 4 phase


## Phase I: vtuber detector

 A script can find virtual youtuber according to twitter friends of a known *"seed"* vtuber.

 actualy I get all my vtuber list from third party data source 
 - [vtuber-post](https://vtuber-post.com/database/)
 - [daifuku](https://mamedaifuku.sakura.ne.jp/)
 data will be saved to `/data`

 **Some other related data in daifuku and socialblade still need to be collected (eg. comment of vtuber, income, ranking)**
 
 **progress:** >>>>>> `PASSING`


## Phase II: data harvest

create a social network (undirected map with value edge) based on following things and the importance is from high to low 
- live together(though youtube api)
- twitter interactive(only one month data will be used)

comment similarity of youtube will alse be collected, this will not be shows in graph but will be use in modeling

**progress:** >>>>>> `FAILING`

## Phase III: Build Model & Data analysis

implememt k-means algorithm to cluster existing networkx-lib with skilearn lib 

## Phase VI: Visualization
using java spring boot to just expose the data in mongodb, it is just used as a api-like too for data virtulize

using D3.js to implement a  front end page

--------------------------

# HOW TO SET UP ENV

### python

For mac:
``` 
$brew install pyenv
# after you intall set environment variable in your ~/.bash_profile
$pyenv install 3.5.6
$pyenv local 3.5.6
# enter root folder of project
$pip install -r requirements.txt
```

### MongoDB

```
# if docker is not installed, plz install docker and docker-compose
$docker pull mongo
# make a workspace/data under '~', then back to project folder
# plz tell me if you need my data
$. ./run_mongo.sh
```

# Java
plz use Intellij Idea
