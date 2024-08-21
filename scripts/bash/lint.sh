#!/bin/sh

echo "Analyzing applications directory..."
pylint applications

echo "Analyzing backend directory..."
pylint backend