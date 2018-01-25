{
  pkgs ? import <nixpkgs> {},
  bash ? pkgs.bash,
  python ? pkgs.python,
  stdenv ? pkgs.stdenv,
  pythonPackages ? pkgs.python27Packages }:


(python.withPackages (ps: [ps.requests])).env
