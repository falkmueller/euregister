<?php

namespace src\component;

class notFoundHandler {

    public static function create($container){
        return new self();
    }

    public function __invoke($request, $response){
        $response = new \Slim\Http\Response(404);
        return $response->write("Page not found");
    }
    
}