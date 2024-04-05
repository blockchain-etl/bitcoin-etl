{
  description = "bitcoin-etl";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }@inputs: {
    nixosModules.etf-scraper = import ./module.nix;
  } //
  flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
      };
    in
    {
      packages.bitcoin-etl = pkgs.python3Packages.buildPythonPackage {
        pname = "bitcoin-etl";
        version = "1.5.2";
        src = self;
        doCheck = false;
      };

      defaultPackage = self.packages.${system}.bitcoin-etl;

      devShells.default = pkgs.mkShell {
        buildInputs = [ pkgs.python3Packages.python pkgs.git ];
        # Include any other development tools you need
      };

    }
  );
}
