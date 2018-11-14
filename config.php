<?php

return [
    'settings' => [
        'view' => [
            "path" => __dir__."/views",
            "ext" => "phtml"
        ],
        'components' => [
            "notFoundHandler" => "src\\component\\notFoundHandler::create",
            "view" => "src\\component\\view::create",
        ],
        'routes' => [
            "home" => [
                "map" => ['GET', 'POST'],
                "route" => "/",
                "callable" => "src\\bootstrap::route",
            ],
            "controller" => [
                "map" => ['GET', 'POST'],
                "route" => "/{controller}[/]",
                "callable" => "src\\bootstrap::route",
            ],
            "action" => [
                "map" => ['GET', 'POST'],
                "route" => "/{controller}/{action}[/{params:.*}]",
                "callable" => "src\\bootstrap::route",
            ],
        ]
    ],
];
