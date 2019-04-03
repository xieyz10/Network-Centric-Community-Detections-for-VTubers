vtuberminer
======================================

This is a vtuber analysis project ~~~~

Hi every DD~~~

--------------------------------------

## Environment:
- Java 8
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

 actualy I get all my vtuber list from a third party data source [vtuber-post](https://vtuber-post.com/database/)
 
 data will be saved to `/data`
 
 **progress:** >>>>>> `PASSING`


## Phase II: data harvest

create a social network (undirected map with value edge) based on following things and the importance is from high to low 
- live together(though youtube api)
- twitter interactive(only one month data will be used)

comment similarity of youtube will alse be collected, this will not be shows in graph but will be use in modeling

**progress:** >>>>>> `FAILING`

## Phase III: Build Model & Data analysis


## Phase VI: Visualization

