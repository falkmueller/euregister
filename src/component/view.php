<?php

namespace src\component;

class view {
    
    public static function create($container){
        $templates = new \League\Plates\Engine(
                $container->get('settings')['view']["path"], 
                $container->get('settings')['view']["ext"]
                );

        $templates->registerFunction('asset', function ($string) use ($container) {
            return  $container->get('router')->pathFor("home").$string;
        });
        
        $templates->registerFunction('url', function ($name, $params = []) use ($container) {
            return  $container->get('router')->pathFor($name, $params);
        });
        
        return $templates;
    }
        
}
