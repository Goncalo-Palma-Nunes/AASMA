{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs:
    inputs.flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import inputs.nixpkgs { inherit system; };
      in
      {
        devShell = pkgs.mkShell {
          hardeningDisable = [ "all" ];

          packages = with pkgs; [
            (python39.withPackages (ps: [
              ps.pygame
              ps.matplotlib
            ]))
          ];
        };
      });
}
