library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;

entity TempDisplay is
    port (
        binInput  : in  std_logic_vector(8 downto 0);
        hex5      : out std_logic_vector(6 downto 0);
		  hex6      : out std_logic_vector(6 downto 0);
		  hex7      : out std_logic_vector(6 downto 0)
    );
end TempDisplay;

architecture Behavioral of TempDisplay is
	signal tempValue : integer range 0 to 511;
begin

	 tempValue <= to_integer(unsigned(binInput));

    with (tempValue rem 10) select
        hex5 <= "1000000" when 0,
                "1111001" when 1,
                "0100100" when 2,
                "0110000" when 3,
                "0011001" when 4,
                "0010010" when 5,
                "0000010" when 6,
                "1111000" when 7,
                "0000000" when 8,
                "0010000" when 9,
                "1000000" when others;
					 
	with ((tempValue / 10) rem 10) select
        hex6 <= "1000000" when 0,
                "1111001" when 1,
                "0100100" when 2,
                "0110000" when 3,
                "0011001" when 4,
                "0010010" when 5,
                "0000010" when 6,
                "1111000" when 7,
                "0000000" when 8,
                "0010000" when 9,
                "1000000" when others;
					 
	with (tempValue / 100) select
        hex7 <= "1000000" when 0,
                "1111001" when 1,
                "0100100" when 2,
                "0110000" when 3,
                "0011001" when 4,
                "0010010" when 5,
                "1000000" when others;
					 
end Behavioral;
