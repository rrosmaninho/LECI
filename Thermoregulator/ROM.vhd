library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;

entity ROM is
	port(address : in  std_logic_vector(19 downto 0);
		  dataOut : out positive);
end ROM;

architecture Behavioral of ROM is
	signal s_weekDay  : positive := 1;
	signal s_hours    : positive := 1;
	signal s_minutes  : positive := 1;
	signal s_position : natural  := 0;

	subtype TDataTemp is positive;
	type TROM is array (0 to 47) of TDataTemp;
	constant week_cycle    : TROM := (4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
												 16, 16, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
												 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
												 16, 16, 16, 16, 4, 4, 4, 4, 4, 4, 4, 4);
	constant weekend_cycle : TROM := (4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 16, 16,
												 16, 16, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
												 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
												 16, 16, 16, 16, 16, 16, 4, 4, 4, 4, 4, 4);
	
begin
	s_weekDay <= to_integer(unsigned(address(19 downto 17)));
	s_hours <= to_integer(unsigned(address(16 downto 12))) + 1;
	s_minutes <= to_integer(unsigned(address(11 downto 6)));
	s_position <= s_minutes/30;
	
   dataOut <= week_cycle(s_hours + s_position) when (s_weekday <= 5) else
				  weekend_cycle(s_hours + s_position);
end Behavioral;
