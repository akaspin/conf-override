# conf-override

Simple configuration templating.

## Problem

Some `.conf` files has inappropriate syntax for including. For example, 
[HAProxy](http://haproxy.1wt.eu/) `conf` syntax is based on blocks that 
accumulates directives. Like this ...

    frontend main
        bind *:80
        acl ...
        use_backend ..
        
    backend one
        ...
        
... Route rules are gathered in `frontend` block. And you can't use very 
convenient `conf.d` paradigm from *NginX* or *Apache*.

## Usage

Solution that can be overrides. You have one `base` file with some directives 
and a lots of `override` files. For example, for the situation described 
above, base file can looks like (/etc/haproxy/haproxy-base.conf):

    # +++ /home/*/haproxy.conf.d/*.conf
    # +++ /etc/haproxy/conf.d/* /anyother/*

    frontend web
        bind *:80
        # <<< ACL_WEB
        # <<< USE_WEB
        default_backend def_backend

    # Default backend
    backend def_backend
        ...
    
    # <<< BACKEND
    
And you can make `overrides` like this:

    # <<< ACL_WEB
        acl is_mybackend ...
    # <<< USE_WEB
        use mybackend if is_mybackend
    # <<< BACKEND
    backend mybackend
        ...
        
... and this:

    # <<< ACL_WEB
        acl is_otherbackend...
    # <<< USE_WEB
        use otherbackend if is_otherbackend
    # <<< BACKEND
    backend otherbackend
        ...
    
... Run `conf-override`:

    python conf-override.py /etc/haproxy/haproxy-base.conf > haproxy.conf
    
... And voila:

    frontend web
        bind *:80
        acl is_mybackend ...
        acl is_otherbackend...
        use mybackend if is_mybackend
        default_backend def_backend

    # Default backend
    backend def_backend
        ...
    
    backend mybackend
        ...
    backend otherbackend
        ...

`conf-override` collect all override files and evaluates all blocks in them.

## Syntax

`conf-override` has two directives: gather and block. All directives should 
follow marker. By default marker is `#`.

Gather directive denoted by triple plus:

    # +++ /home/*/haproxy.conf.d/*.conf /anyother/*
    
The arguments of this directive is set of paths. Paths can contain wildcards. 
This directive can only appear in base file.

Block directive can appear in both base and override files. It denotes by 
tripple `<` symbols.

    # <<< BLOCK
    
This directive as one argument - block name.

## Marker

By default marker is `#`. To change it just run `conf-override` with `-m` 
option:

    python conf-override.py -m / ...
    
... or long `--marker` option:

    python conf-override.py -marker=/ ...
    
## Warnings

There is no syntax checking. All overrides processes in alphabetical order. 
Be wise. 
  

