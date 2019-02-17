
@Radek napisał:
===============

"In my opinion, users should be treated as customers. In the case of EOS
Factory, users are developers. Their convenience is more important than the
mentioned readability (for non-programmers) or brevity. It is also not a good
idea to try to convince the community to change their habits. It is a hopeless
task."

Nie chcę komentować tej opinii publicznie, dlatego tutaj.

Ja uważam, że deweloperzy nie są naszymi klientami (ale niech ta opinia pozostanie między nami). 
Deweloperów jest niewielu. Deweloperzy "have their habits" i rzadko szukają nowinek w rodzaju narzędzi, oferowanych w przytłaczającym nadmiarze wyboru.

Tokenika nie przeżyje ze sprzedaży narzędzi deweloperskich -- bo też nie ma takich. Tokenika żyje z publicity.

EOSFaktory dla entuzjastów
^^^^^^^^^^^^^^^^^^^^^^^^^^

Klientami EOSFactory mogą być zainteresowani amatorzy -- entuzjaści świata blockchainowego bezpieczeństwa (urojonych?) prywatnych sekretów.

Dla tych entuzjastów -- najlepsi wśród nich dają nam gwiazdki (204 teraz, 4 na tydzień, nie ma pewnie tylu deweloperów smart-kontraktów na całym świecie) -- powinniśmy urządzać EOSFactory w stylu najbardziej przez nich pożądanym. 

EOSFactory dla entuzjastów powinien dawać możliwość łatwego nawiązania kontaktu (mentalnego) z blockchainem i dać bazę łatwej wiedzy. Musi być łatwy, zwięzły i kolorowy.

EOSFactory dla entuzjastów powinien organizować community: szukać amatorów propagowania idei wiedzy o EOSIO, proponować konkursy amatorskich smart-kontraktów pisanych w stylu EOSIde (o tym -- dalej), prowadzić warsztaty dobrego stylu.

Jak budować EOSFactory dla entuzjastów?
---------------------------------------

Potrzebny jest animator środowiska. Jak znaleźć takiego? Nie wiem, ale uważam, że wiem jak nie szukać: nie jest tu istotną kwalifikację doświadczenie w pracy z Pythonem. 

Wiemy już, że pythonowiec-koder łatwo koncentruje się na prostym aspekcie technicznym, takim jak dystrybucja PyPi albo kwestia globalności deklaracji obiektów kont EOSIO (bo to -- wydaje mu się -- jest łatwe i już to umie), podczas gdy my chcemy zyskać publicity, a do tego potrzebne jest rozumienie funkcjonalności EOSFactory i umiejętność dyskusji na tym poziomie.

Na pewno, można znaleźć kwestie techniczne wymagające opracowania, ale takie ja sam obsłużę. Przykładem jest dystrybucja PyPi, już gotowa w tydzień, zamiast być niegotowa w trzy miesiące, bo @noisy nie miał możliwości zrobić tego bez wysiłku w zrozumienie działania całego systemu.

Nasz człowiek może znalazłby się wśród młodych gików. Potrzebna jest swoboda językowa i entuzjazm, ale brak doświadczenia (i rutyny) byłby atutem. Odpowiednią wiedzę uzyskałby od nas.

EOSFactory dla właścicieli kont EOSIO
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Od samego początku zakładałem, że EOSFactory nie jest dla rutyniarzy IT: dlatego Python jest wybranym językiem. Mimo że Python jest używany w profesjonalnych zakładach deweloperskich (tam w znacznym stopniu przeciwko duchowi języka nawiązującego do lekkiej atmosfery latającego cyrku Monty Pythona), jego styl jest specjalnie nie-specjalnie profesjonalny.

Założycielską idea Pythona jest to, że stylowy skrypt czyta się tak (niemal) jak naturalny angielski: mało w nin znaków kodowych.

Wiemy, że smart-kontrakty są przeznaczone istnieć na pograniczu sfer formalno-prawnych i IT. W najbardziej wymagającym zastosowaniu, smart-kontrakt może być techniczno-informatycznym odwzorowanie formalno-prawnej umowy pomiędzy osobami prawnymi. W technologii EOSIO ten związek jest ustalony przez Ricardian Contract, wymagany element kontraktu. Ricardian Contract łączy też dewelopera IT z właścicielem kont EOSIO: jest protokołem przekazania wyrobu.

Każdy może zobaczyć przykład Ricardian Contract dla eosio hello.

No więc wybór języka polegał na możliwości, że kod testów wyrażone pythonem byłyby zawarte w Ricardian Contract. Wtedy tekst Ricardian Contract pozostawałby zrozumiały dla nie-programisty i jednocześnie byłby wykonywalnym testem poprawności biznesowej kontraktu.

Jak budować EOSFactory dla właścicieli kont EOSIO?
--------------------------------------------------

Myślę, że @Marcin Zientek podołałby.

@Jakub: Niestety nie mamy roadmap
=================================

Rozważcie co napisałem powyżej. Ponadto EOSIde.

EOSIed
^^^^^^

Pewnie tylko @Jakub wie, że istnieje. 

Ten projekt jest zgodny z moją koncepcją sprzedawalności EOSFactory (zobacz '@Radek napisał:'), podczas gdy @Jakub polega na mniemaniu, że EOSFactory chce być narzędziem deweloperów, a od ludzi wie, że deweloperzy (którzy nie są naszymi klientami, choć nie powinniśmy tego ogłaszać) nie potrzebują IDE (Integrated Development Environment). Dlatego @Jakub, zapracowany pilnymi obowiązkami, nie ma czasu na pojęcie EOSIed. 

(Jeszcze jeden powód dlaczego EOSFactory nie może teraz być narzędziem dla developerów: trzeba być developerem smart-kontraktów (w tym choć jednego wielkiego), żeby poznać, że to, co się zrobiło jest narzędziem dla deweloperów.)

EOSIde jest środowiskiem programistycznym przeznaczonym do wypełnienia postulatów przedstawionych w tekście '@Radek napisał:'. 

README https://github.com/tokenika/eoside daje pojęcie o projekcie. EOSIde jest rozszerzeniem do VSCode. Stan gotowości do publikacji jest "niemal".

Pierwszym opublikowanym zastosowaniem EOSIde będzie przetworzony tutorial 'Elemental Battles'.
