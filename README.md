pond
====

A Python script for managing groups of Digital Ocean droplets

### Prerequisites

#### 0. Python

Make sure that Python is installed on your system. This script has been verified again Python 2.7

#### 1. dopy

Pond has a dependency on the ```dopy``` library. 

```
# pip install dopy
```

#### 2. Digital Ocean client id and api key

Pond expects to find your Digital Ocean client id and api key in the environment variables ```DO_CLIENT_ID``` and ```DO_API_KEY```



### Usage

#### 0. Clone Pond

```
# git clone https://github.com/kchard/pond.git
```

#### 1. Verify Setup

```
# python pond.py 
```

OR

```
# chmod +x pond.py
# ./pond.py
```

If your client id or api key are not defined you will get an error. Otherwise you should see the usage message:

```
Usage: pond.py pond (fill|drain|refill)
```

#### 2. Define a pond

Create a json file called ```example.json``` with the following contents:

```
{
  "pond_name": "example",
  "droplets": [
    {
      "config": {
        "name" : "small-droplet",
        "size_id" : "66",
        "image_id" : "303619",
        "region_id" : "3",
        "ssh_key_ids" : "45038"
      },
      "num": 1
    }
  ]
}
```

The ```num``` property determines the number of droplets that will be created with the given configuration. You can speficy more than one item in the ```droplets``` list if you need to define droplets with different properties.

#### 3. Fill your pond

```
# ./pond.py example.json fill
```

By default, ```pond``` will store your droplet information in ```~/.ponds/[pond_name]/.pond```.

```
# cat ~/.ponds/example/.pond
```

You should see a map from the ip address of each droplet to its id.



#### 4. Drain your pond

```
# ./pond.py example.json drain
```

Drain will destroy all of the droplets in your pond and delete the pond directory.

```
find ~/.ponds
```

You should no longer see the ```~/.ponds/example``` directory.



