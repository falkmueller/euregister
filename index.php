<?php

require_once './vendor/autoload.php';

/* init application */
$app = new \Slim\App(require './config.php');

/* load components */
$container = $app->getContainer();
foreach ($container->get('settings')['components'] as $name => $callable){    
   $container[$name] = function($c)use($callable){ 
        return call_user_func($callable, $c); 
    };
}

/* init routes */
foreach ($container->get('settings')['routes'] as $name => $options){ 
    $app->map($options["map"], $options["route"], $options["callable"])->setName($name);
}

/* run application */
$app->run();