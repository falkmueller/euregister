<?php

namespace src\controller;

class infoController {
    
    private $_container;
    
    public function __construct($container){
        $this->_container = $container;
    }
    
    public function indexAction($request, $response, $args){
        return $response->write($this->_container->view->render("info"));
    }
    
}
