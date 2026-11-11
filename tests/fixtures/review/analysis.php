<?php

declare(strict_types=1);

/** @param list<int> $ids */
function firstId(array $ids): int
{
    return $ids[0] ?? null;
}
