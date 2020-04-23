# El joc de la vida

El [joc de la vida](https://ca.wikipedia.org/wiki/Joc_de_la_vida) és un autòmat cel·lular dissenyat pel matemàtic britànic John Horton Conway el 1970. He volgut desenvolupar-lo en python per aprendre els conceptes més bàsics de [pygame](https://www.pygame.org/).

<img src="https://pribaq.net/fotos/joc-de-la-vida.gif" width="500px">

## Les normes del joc:

 1. Tota cel·la viva amb menys de dos veïns vius mor (de solitud)
 2. Tota cel·la viva amb més de tres veïns vius mor (de sobrepoblació).
 3. Tota cel·la viva amb dos o tres veïns vius, segueix viva per a la següent generació.
 4. Tota cel·la morta amb exactament tres veïns vius torna a la vida.