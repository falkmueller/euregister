<?php

namespace src;

class bootstrap {
    
    public static function route($request, $response, $args){
        global $app;
        $container = $app->getContainer();
        
        $controllerName = !empty($args["controller"]) ? $args["controller"]: "index"; 
        $actionName = !empty($args["action"]) ? $args["action"]: "index"; 
        $params = !empty($args["params"]) ? explode("/", $args["params"]) : [];
        
        $controllerClass = "\\src\\controller\\{$controllerName}Controller";
        
        if(!class_exists($controllerClass)){
            $notFoundHandler = $container->get('notFoundHandler');
            return $notFoundHandler($request, $response);
        }
        
        $controller = new $controllerClass($container);
        
        $methode = "{$actionName}Action";
        if(!method_exists($controller, $methode)){
            $notFoundHandler = $container->get('notFoundHandler');
            return $notFoundHandler($request, $response);
        }
        
        return call_user_func_array([$controller, $methode],[$request, $response, $params]);
    }
    
}
