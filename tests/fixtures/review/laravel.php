<?php

// Illustrative review snippets. This file is never registered as application routes.

function displayOrder(int $id): mixed
{
    return \App\Models\Order::findOrFail($id);
}

function authorNames(iterable $books): array
{
    $names = [];
    foreach ($books as $book) {
        $names[] = $book->author->name;
    }

    return $names;
}

function createOrder(\Illuminate\Http\Request $request): mixed
{
    return \App\Models\Order::create(['quantity' => $request->input('quantity')]);
}
