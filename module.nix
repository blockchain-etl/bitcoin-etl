flake: { config, lib, pkgs, ... }:

with lib;

let
  inherit (flake.packages.${pkgs.stdenv.hostPlatform.system}) bitcoin-etl;

  cfg = config.services.bitcoin-etl;
in
{
  options.services.bitcoin-etl = {
    enable = mkEnableOption "Bitcoin ETL service";
  };

  config = mkIf cfg.enable {

    users = {
      users.bitcoin-etl = {
        isSystemUser = true;
        group = "bitcoin-etl";
        home = "/home/bitcoin-etl";
        createHome = true;
        homeMode = "755";
      };
      groups.bitcoin-etl = { };
    };

    systemd.timers.bitcoin-etl = {
      description = "Timer for Bitcoin ETL Service";
      wantedBy = [ "timers.target" ];
      after = [ "bitcoin-etl.service" ];
      timerConfig = {
        OnCalendar = "hourly";
        Unit = "bitcoin-etl.service";
      };
    };

    systemd.services.bitcoin-etl = {
      description = "Bitcoin ETL Service";
      # service should only run when scheduled, not when system is booted so no
      # wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ];
      script = ''
        ${bitcoin-etl}/bin/bitcoin-etl \
          ${if cfg.exportBlocks then "--export-blocks" else "--no-export-blocks"} \
      '';

      serviceConfig = {
        Restart = "on-failure";
        MemoryDenyWriteExecute = true;
        ReadWriteDirectories = "/home/bitcoin-etl/";
        DynamicUser = true;
        User = "bitcoin-etl";
        Group = "bitcoin-etl";
      };
    }; # systemd.services.bitcoin-etl
  }; # config
}
