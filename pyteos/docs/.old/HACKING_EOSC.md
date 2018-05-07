### create key
/mnt/hgfs/Workspaces/EOS/eos/programs/eosioc/main.cpp 473 create->add_subcommand
  private_key_type::generate();
    /mnt/hgfs/Workspaces/EOS/eos/libraries/fc/include/fc/crypto/private_key.hpp
      /mnt/hgfs/Workspaces/EOS/eos/libraries/fc/include/fc/crypto/elliptic.hpp
        /mnt/hgfs/Workspaces/EOS/eos/libraries/fc/src/crypto/elliptic_common.cpp
          /mnt/hgfs/Workspaces/EOS/eos/libraries/fc/src/crypto/elliptic_openssl.cpp

mnt/hgfs/Workspaces/EOS/eos/programs/eosioc/main.cpp 473 create->add_subcommand
  string(pk.get_public_key());
    /mnt/hgfs/Workspaces/EOS/eos/libraries/fc/src/crypto/private_key.cpp
      /mnt/hgfs/Workspaces/EOS/eos/libraries/fc/include/fc/static_variant.hpp
        eosc/libraries/fc/src/public_key.cpp