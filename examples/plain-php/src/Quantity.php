<?php

declare(strict_types=1);

namespace Example;

final class Quantity
{
    public function __construct(public readonly int $value)
    {
        if ($value < 1) {
            throw new \InvalidArgumentException('Quantity must be positive.');
        }
    }
}
