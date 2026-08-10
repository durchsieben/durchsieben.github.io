---
title: "Qualitätsrezepte für Softwarearchitekturen"
date: "2010-10-08 08:00:48"
sourcePath: "/2010/10/08/qualitatsrezepte-fur-softwarearchitekturen/"
sourceUrl: "https://durchsieben.de/2010/10/08/qualitatsrezepte-fur-softwarearchitekturen/"
wordpressId: "468"
---
<p style="padding-left:30px;">Manch ein Softwaresystem bietet alle geforderten Funktionen und stellt den Kunden dennoch nicht zufrieden. Und dies nur deshalb, weil der Architekt nichtfunktionale Anforderungen wie Geschwindigkeit oder die Sicherheit der Anwendung bei der Planung vernachlässigt hat. Konkrete Strategien und Taktiken können das verhindern.</p>
Bob, der Softwarearchitekt, wirkt seit Stunden deprimiert und nachdenklich. Als ihn seine Kollegen daraufhin ansprechen, erläutert er die Ursache seiner schlechten Laune.<!--more--> Schon wieder ist ein wichtiges Kundenprojekt in Schieflage geraten. Und erneut waren nicht die funktionalen Anforderungen der Hauptgrund, sondern die nichtfunktionalen Qualitäten. Das System ist schlicht zu langsam, hat diverse Sicherheitslücken und stürzt beim kleinsten Problem ab.

Warum nur geraten Architekten und Entwickler immer in dieselben Fallstricke, fragt sich Bob. „Lernen aus Fehlern" klingt zwar gut, rein theoretisch betrachtet, aber beim Praktizieren hapert es noch. Da helfen auch alle Worte des Trostes nur bedingt. Seine Laune verbessert sich erst, als ihm Alice erzählt, wie sich nichtfunktionale Qualitäten gezielt umsetzen lassen.
<p style="text-align:right;"><strong>Alles, klar, nach Anforderung</strong></p>
Zuerst unternimmt Alice einen kleinen Abstecher in die Welt der Requirements. Jeglicher systematische Entwurf einer Softwarearchitektur folgt einem anforderungsgetriebenen Ansatz. Das heißt, eine bestimmte Architekturentscheidung kommt nur dann zustande, wenn dafür mindestens eine Anforderung existiert. Andernfalls würde sich die Gefahr unnützer Funktionen und damit selbstverschuldeter Komplexität (Accidental Complexity) spürbar erhöhen. Ohne vernünftige Anforderungen kann es folglich keine vernünftige Softwarearchitektur geben.

Doch was ist eigentlich eine Anforderung? Laut Definition repräsentiert sie eine einzelne, dokumentierte Aussage darüber, was ein Produkt oder Dienst sein oder tun soll. Mit anderen Worten, jede Anforderung identifiziert eine notwendige Eigenschaft, Fähigkeit oder Qualität eines Systems, deren Vorhandensein die Software für einen Benutzer wertvoll und nützlich macht.

Leider gibt es eine ganze Latte verschiedener Arten von Requirements. Und noch dazu eine unüberschaubare Menge verbreiteter Taxonomien. So subsumiert der Begriff „Kundenanforderungen“ oft sowohl Funktionen als auch Anwendungsfälle (Use Cases) und Qualitätseigenschaften, die sogenannten nichtfunktionalen Eigenschaften. Wichtig ist aber nicht die Klassifizierung von Anforderungen, sondern dass sie möglichst vollständig und konkret vorliegen.

Requirements können also nur dann als Basis eines fundierten Entwurfs dienen, wenn ihre Beschreibungen gewisse innere Qualitäten aufweisen. So sollten Anforderungsbeschreibungen
<ul>
	<li>sich auf eine Sache beschränken,</li>
	<li>vollständig — also ohne fehlende Information — vorliegen,</li>
	<li>Konsistenz zeigen und somit keinen anderen Anforderungen widersprechen,</li>
	<li>korrekt sein,</li>
	<li>Aktualität besitzen, also nicht längst überholt sein,</li>
	<li>eine vom Nutzer beobachtbare Eigenschaft beschreiben,</li>
	<li>innerhalb der Rahmenbedingungen umsetzbar sein,</li>
	<li>eindeutig formuliert sein und nicht etwa in Form nebulöser Beschreibungen vorliegen,</li>
	<li>verpflichtende Eigenschaften des Systems repräsentieren und</li>
	<li>eine Verifizierung, ermöglichen.</li>
</ul>
<p style="text-align:right;"><strong>Das nichtfunktionale Universum</strong></p>
„Nichtfunktional“ leitet sich vom englischen Wort „nonfunctional“ ab, was leider eine äußerst dumme Sache ist. Lässt sich darunter doch zumindest im Englischen auch ein System begreifen, das nicht funktioniert. Daher ist in diesem Zusammenhang häufig stattdessen von Qualitätseigenschaften die Rede. Eine nützliche Untergliederung dieser Anforderungen ist die in operationale und entwicklungsspezifische. Während Erstere Einfluss auf das Laufzeitverhalten haben, etwa auf Performanz, Verfügbarkeit oder Sicherheit, wirken sich Letztere eher auf die Softwareentwicklung aus, beispielsweise auf die Änderbarkeit. Der praktische Umgang mit Qualitäten erweist sich deshalb als komplex, weil sie zum einen verschiedene Facetten besitzen und sich zum anderen als Querschnittsbelange mit systemischer Breitenwirkung herauskristallisieren. Operationale Qualitäten wie Sicherheit oder Performanz lassen sich nun mal nicht durch einzelne lokale Artefakte umsetzen — leider.

Gewöhnlich hat eine operationale Eigenschaft wie Performanz zudem viele unterschiedliche Aspekte: Durchsatz, Antwortzeit, Ein-/Ausgabegeschwindigkeit, beobachtbare Geschwindigkeit, Hochfahrzeit oder Skalierbarkeit (siehe Abbildung 1).

[caption id="attachment_472" align="alignleft" width="420"]<a href="/media/2010/09/abb10.png"><img class="size-full wp-image-472 " title="abb10" src="/media/2010/09/abb10.png" alt="Abbildung 1: Qualitätseigenschaften haben typischerweise viele Facetten und können sich gegenseitig in die Quere kommen" width="420" height="360" /></a> Abbildung 1: Qualitätseigenschaften haben typischerweise viele Facetten und können sich gegenseitig in die Quere kommen[/caption]

Und ebenso besitzen entwicklungsspezifische Eigenschaften wie Modifizierbarkeit diverse Facetten: Adaptierbarkeit, Ersetzbarkeit, Erweiterbarkeit, Entfernbarkeit, Wiederverwendung, Agilität, Modularität oder Konfigurierbarkeit. Daher müssen Softwarearchitekten mit anderen Beteiligten genau klären, was die einzelnen Qualitäten im Projekt konkret zu bedeuten haben. Eine Aussage wie „das System muss eine hohe Geschwindigkeit aufweisen“, sind nahezu wertlos und nicht verifizierbar. Noch dazu bremsen sich manche Qualitäten gegenseitig aus. Hohe Flexibilität könnte etwa die Einführung verschiedener Indirektionsstufen bedeuten, während hohe Performanz oft mit einer Reduktion von Indirektionsstufen einhergeht. Wegen solcher Konflikte erweist sich die eindeutige Priorisierung von Anforderungen als essenziell, Ein weiteres berühmtes Beispiel stellt das CAP Theorem (Consistency, Availability, Partition Tolerance) von Eric Brewer dar, demzufolge ein System höchstens zwei der genannten Qualitäten aufweisen kann, niemals aber alle drei. Wer übrigens mal einen Überblick über mögliche Qualitäten gewinnen möchte — man gönnt sich ja sonst nichts — möge im Web nach ISO 9621 suchen.
<p style="text-align:right;"><strong>In Szenarien denken</strong></p>
Für den systematischen Umgang mit funktionalen Aspekten eines Softwaresystems haben sich speziell die sogenannten Anwendungsfälle bewährt. Das System selbst stellt sich der Softwarearchitekt oder Anforderungsverantwortliche hierbei als schwarzen Kasten vor, dessen Innereien er nicht kennt. Anhand dieses Modells überlegt er, welcher Akteur von außen welche Ereignisse — also welche Szenarien — beim System auslösen kann und mit welchen externen Akteuren das System zu diesem Zweck zusammenspielen muss, Dabei kann ein Akteur sowohl menschlicher als auch nichtmenschlicher Art sein, etwa ein externes IT-System.

Das Denken in Szenarien ist derart hilfreich und flexibel, dass sich dieses Konzept mit ein paar Adaptionen für die Behandlung nichtfunktionaler Eigenschaften ebenfalls eignet. Das allgemeine Szenariodiagramm in Abbildung 2 soll die Idee verdeutlichen.

[caption id="attachment_473" align="alignleft" width="440"]<a href="/media/2010/09/abb20.png"><img class="size-full wp-image-473 " title="abb20" src="/media/2010/09/abb20.png" alt="Abbildung 2: Mithilfe von Szenarien lassen sich nichtfunktionale Qualitäten anwendungsnäher und damti spezifischer betrachten" width="440" height="160" /></a> Abbildung 2: Mithilfe von Szenarien lassen sich nichtfunktionale Qualitäten anwendungsnäher und damti spezifischer betrachten[/caption]

Ein Verursacher sendet einen Stimulus an ein System oder einen Systemteil. Besagtes Artefakt kann sich dabei in verschiedenen Zuständen befinden, was das Attribut Umgebung ausdrücken soll. Auf den Stimulus reagiert das System mit einer Antwort beziehungsweise Aktivität, der man eine Messgröße zuordnen kann.

Was etwas abstrakt erscheint, erschließt sich anhand eines konkreten Beispiels. In dem gewählten Szenario (Abbildung 3) versucht ein anonymer Nutzer, auf Systemdienste zuzugreifen, ohne dazu berechtigt zu sein.

[caption id="attachment_474" align="alignleft" width="440"]<a href="/media/2010/09/abb30.png"><img class="size-full wp-image-474 " title="abb30" src="/media/2010/09/abb30.png" alt="Abbildung 3: Das Beispiel eines Sicherheitsszenarios verdeutlicht mögliche Schwachpunkte eines Systems" width="440" height="222" /></a> Abbildung 3: Das Beispiel eines Sicherheitsszenarios verdeutlicht mögliche Schwachpunkte eines Systems[/caption]

Als Reaktion auf diesen Stimulus blockiert das System den Zugriff und protokolliert zugleich die auffälligen Aktivitäten. Die Reaktion lässt sich nun durch zwei Größen quantifizieren:

Zum einen anhand der Wahrscheinlichkeit, dass es zur Aufdeckung solcher nicht autorisierter Zugriffe kommt, und zum anderen anhand der Prozentzahl der trotz Angriffe noch verfügbaren Dienste.

Insgesamt bewirken solche Szenarien, dass man über die Qualitäten eines Systems anhand konkreter Abläufe nachdenken kann, statt sich auf einem nebulösen Level zu bewegen. Und als netter Zusatzeffekt führt das Denken in Szenarien dazu, ein besseres Bild davon zu gewinnen, wie sich die Softwarearchitektur beispielsweise durch Tests verifizieren lässt.
<p style="text-align:right;"><strong>Mein Freund,der Qualitätsbaum</strong></p>
Softwarearchitekten, die solche Szenarien nutzen, entwerfen zunächst einen sogenannten Utility-Tree für das Projekt (Abbildung 4).
<p style="text-align:center;"></p>


[caption id="attachment_475" align="aligncenter" width="600"]<a href="/media/2010/09/abb40.png"><img class="size-full wp-image-475 " title="abb40" src="/media/2010/09/abb40.png" alt="Abbildung 4: Ein Qualitätsbaum (Utility Tree) hilft, gewünschte Qualitäten bis auf Szenarien herunterzubrechen und zu bewerten" width="600" height="340" /></a> Abbildung 4: Ein Qualitätsbaum (Utility Tree) hilft, gewünschte Qualitäten bis auf Szenarien herunterzubrechen und zu bewerten[/caption]

Auf dessen linker Seite befinden sich spezifische Qualitäten wie Performanz, Sicherheit oder Verfügbarkeit. Wie erwähnt, sind diese generisch und bedürfen daher einer genaueren Untergliederung. In konkreten Projekten — etwa einem Online-Videoportal — gibt es zwei wichtige Aspekte für die Gewährleistung von Performanzz die Latenzzeit beim Datenzugriff und die Zahl der Transaktionen

pro Zeiteinheit. Allerdings erweist sich diese Untergliederung immer noch als zu grobkörnig, denn was genau soll etwa die Latenzzeit beim Datenzugriff bedeuten? Hierfür kommen die Szenarien ins Spiel. Für jede gewünschte Performanzeigenschaft spezifizieren Softwarearchitekten ein oder mehrere projektspezifische Szenarien, mit deren Hilfe sie prüfen können, ob das System die gewünschte Systemqualität erfüllt. Im konkreten Fall soll die Speicherlatenz der Kundendatenbank weniger als 200 Millisekunden betragen. Zugleich muss das Transportieren von Videos immer in Echtzeit erfolgen.

Noch einen weiteren Vorteil bieten die Utility-Trees. Im Artikel über systematischen Architekturentwurf (<a href="http://wp.me/pkFkC-82">Systematisches Softwaredesign in der Nussschale</a>) hatte Bob gelernt, dass alle Anforderungen immer eine Priorisierung benötigen. Und auch hierfür können die Mitglieder des Entwicklungsteams sowie das Management den Qualitätsbaum benutzen. In einem Workshop ordnen die Beteiligten jedem Szenario ein Tupel aus zwei Elementen zu. Dessen linke Seite definiert, welche Relevanz das jeweilige Szenario aus Geschäftssicht besitzt, also hoch (H), mittel (M) oder niedrig (N). Die rechte Seite identifiziert, wie komplex die Architekten den Entwurf des Szenarios einschätzen. So ergibt sich sowohl für die geschäftlich orientierten Projektbeteiligten als auch für die

Entwicklungsabteilung ein wichtiger Anhaltspunkt. Dabei lassen sich natürlich auch andere Priorisierungsschemata benutzen, aber das ist unwesentlich.
<p style="text-align:right;"><strong>Strategien gefolgt von Taktiken</strong></p>
Die szenariobasierte Betrachtung ist ja ganz nett, denkt sich Bob, aber wie in aller Welt kommen hier architektonische Entscheidungen ins Spiel? Anders gefragt, wie genau sollen Softwarearchitekten mit nichtfunktionalen Eigenschaften umgehen? Damit die Architektur Qualitäten wie Performanz gewährleistet, sind diverse Ansätze denkbar. Zum Beispiel könnten eine effektive Nutzung und das effiziente Management von Ressourcen wie Threads oder Speicher die Performanz verbessern. In dem Fall wäre Ressourcen-Management eine denkbare Strategien für optimalen Durchsatz. Dummerweise beantworten Strategien nur die Frage nachdem „Was“, nicht aber die Frage nach dem „Wie“ (siehe Abbildung 5).

[caption id="attachment_476" align="alignleft" width="440"]<a href="/media/2010/09/abb50.png"><img class="size-full wp-image-476 " title="abb50" src="/media/2010/09/abb50.png" alt="Abbildung 5: Um eine Qualität wie Performanz oder Sicherheit zu gewährleisten, gibt es mehrere Strategien. Entwurfstaktiken definieren deren konkrete Umsetzung" width="440" height="175" /></a> Abbildung 5: Um eine Qualität wie Performanz oder Sicherheit zu gewährleisten, gibt es mehrere Strategien. Entwurfstaktiken definieren deren konkrete Umsetzung[/caption]

[caption id="attachment_492" align="alignright" width="220"]<a href="/media/2010/10/abb60.png"><img class="size-full wp-image-492 " title="abb60" src="/media/2010/10/abb60.png" alt="Abbildung 6: Designtaktiken helfen bei der Umsetzung nichtfunktionaler Qualitäten" width="220" height="132" /></a> Abbildung 6: Designtaktiken helfen bei der Umsetzung nichtfunktionaler Qualitäten[/caption]

Um eine bestimmte Ausprägung einer Qualität in die Tat umzusetzen, bedarf es sogenannter Entwurfstaktiken. Hier kommen wieder die Szenariodiagramme ins Spiel. Als Antwort auf Stimuli muss die Softwarearchitektur spezifische Taktiken implementieren (siehe Abbildung 6).

Eine Entwurfstaktik spezifiziert dabei eine mögliche Reaktion des Systems. Für ein qualitätsbasiertes Entwurfsziel kann es allerdings viele unterschiedliche Taktiken geben, sodass der Softwarearchitekt die Qualder Wahl hat.
<p style="text-align:right;"><strong>In medias res statt nebulos</strong></p>
Ist zwar alles durchaus interessant, aber auch etwas nebulös, denkt sich Bob, worauf ihm Alice mit einem konkreten Beispiel auf die Sprünge hilft und das Thema Sicherheit genauer unter die Lupe nimmt. Ein eher generisches Szenariodiagramm würde aussehen wie in Abbildung 7.

[caption id="attachment_487" align="alignleft" width="440"]<a href="/media/2010/09/abb701.png"><img class="size-full wp-image-487 " title="abb70" src="/media/2010/09/abb701.png" alt="Abbildung 7: Ein generische Szenariodiagramm konkretisiert sicherheitsrelevante Aspekte" width="440" height="195" /></a> Abbildung 7: Ein generische Szenariodiagramm konkretisiert sicherheitsrelevante Aspekte[/caption]

Angenommen, ein externer Akteur (Verursacher) versucht, verbotenerweise auf Daten oder Dienste zuzugreifen, Daten zu löschen oder zu modifizieren beziehungsweise mit einer DDoS-Attacke (Distributed Denial of Service) die Verfügbarkeit zu reduzieren (Stimulus). Die Daten oder Dienste des Systems (Artefakt) können sich zum Zeitpunkt des „Angriffs“ in verschiedenen Zuständen befinden (Umgebung), etwa online, offline, verbunden oder nicht verbunden. Als Reaktion (Antwort) soll das System nach Meinung des Architekten beispielsweise

den Benutzer zur Authentifizierung zwingen, den Zugriff blockieren, den Angriff protokollieren oder Daten verschlüsseln. Zwei wichtige Messgrößen kommen dabei zum Tragen: die Wahrscheinlichkeit, derartige Verstöße zu bemerken oder die prozentuale Verfügbarkeit des Systems.

[caption id="attachment_493" align="alignleft" width="440"]<a href="/media/2010/10/abb80.png"><img class="size-full wp-image-493" title="abb80" src="/media/2010/10/abb80.png" alt="Abbildung 8: Für die Gewährleistung von Sicherheit stehen Softwarearchitekten und -entwicklern verschiedene Strategien und Taktiken zur Verfügung" width="440" height="278" /></a> Abbildung 8: Für die Gewährleistung von Sicherheit stehen Softwarearchitekten und -entwicklern verschiedene Strategien und Taktiken zur Verfügung[/caption]

Um diese Systemreaktion zu erreichen, stehen den Architekten unterschiedliche Strategien zur Verfügung, die sich wiederum mittels verschiedener Entwurfstaktiken realisieren lassen (siehe Abbildung 8).

„Angriffen widerstehen“ ist die erste Strategie, um es erst gar nicht zu größeren Problemen kommen zu lassen. Dazu gehören folgende Entwurfstaktiken, wobei jede davon eine Option darstellt, die sich mit anderen Taktiken kombinieren lässt:
<ul>
	<li>Authentifizierung der Benutzer</li>
	<li>Benutzern explizit Berechtigungen zuordnen</li>
	<li>Gewährleistung der Vertraulichkeit von Daten</li>
	<li>Sicherung der Integrität, beispielsweise durch Prüfsummen</li>
	<li>Begrenzung des Zugriffs auf die benötigten Dienste</li>
	<li>Beschränkung des Zugriffs, etwa durch Firewalls</li>
</ul>
„Angriffe aufspüren“ heißt die nächste Strategie, deren Taktik das Aufspüren von Eindringversuchen ist. Das lässt sich etwa durch die Analyse von Zugriffsmustern erreichen, indem man sie mit historischen Mustern vergleicht.

Schließlich gibt es eine weitere Strategie, damit ein System sich von Angriffen erholen kann. Sie gruppiert sich in zwei Unterstrategien. Da wäre zum einen die Wiederherstellung korrumpierter Dienste. Diese Unterstrategie ist allerdings gleichbedeutend mit Fehlertoleranzmechanismen, weshalb das Diagramm lediglich auf entsprechende Strategien für Fehlertoleranz verweist. Für die zweite Unterstrategie „Identifikation“ hingegen existiert eine Designtaktik.

Audit Trail bezeichnet die Protokollierung aller Zugriffe auf Dienste und Daten, sozusagen als Spurensicherung. Für die Umsetzung der genannten Entwurfstaktiken sollten Softwarearchitekten gezielt nach Entwurfsmustern Ausschau halten. Da es sich um Probleme handelt, die in vielen Projekten wiederkehren, dürfte es ziemlich wahrscheinlich sein, dass es solche Muster gibt.
<p style="text-align:right;"><strong>Eine Frage der Sensibilität</strong></p>
Aus Gründen der Übersicht sind die hier skizzierten Beispiele sehr allgemein gehalten. In der alltäglichen Praxis würden die Beteiligten sowohl die Szenarien als auch die Strategie- beziehungsweise Taktikdiagramme für den Projektkontext konkretisieren und komplettieren.

Wichtig für Softwarearchitekten ist in diesem Kontext, dass sie die sensiblen Punkte (Sensitivity Points) und Kompromissstellen (Tradeoff Points) in der Softwarearchitektur kennen. Erstere definieren die Kritikalität einer Gruppe zusammengehöriger Komponenten für das Erreichen einer bestimmten nichtfunktionalen Qualität. Kornpromissstellen kennzeichnen die Punkte, die sich für mehr als eine nichtfunktionale Qualität als kritisch erweisen und damit sensible Punkte für die verschiedenen Qualitäten darstellen. Ohne Wissen über derartige Architekturstellen führen spätere Änderungen der Anforderungen oder der Architektur fast garantiert zu Problemen. Normalerweise sollten sich alle entsprechenden Stellen ohnehin automatisch herauskristallisieren, wenn die Softwarearchitekten konsequent einen anforderungsgetriebenen Systementwurf verfolgen.
<p style="text-align:right;"><strong>Fazit</strong></p>
Auf nichtfunktionale Qualitäten sollten Softwarearchitekten und —entwickler ein verstärktes Augenmerk legen. Aufgrund ihres systemischen Charakters verursachen diese Aspekte in den meisten Projekten Probleme. Aus diesem Grund sollte die Liste der funktionalen und nichtfunktionalen Anforderungen ausreichend klar, in hoher Qualität und priorisiert vorliegen. Dafür nutzen Architekten am besten Utility-Trees, die sie gemeinsam mit anderen Beteiligten erstellen, um ein gemeinsames (Ein)Verständnis zu erzielen. Als positiver Nebeneffekt fallen hinterher die Qualitätsprüfung und das Testen leichter.

Wie sich die Erstellung von Softwarearchitekturen systematisieren lässt, hat der Artikel <a href="http://wp.me/pkFkC-82">Systematisches Softwaredesign in der Nussschale</a> bereits ausführlich beschrieben.

Für das schrittweise Integrieren operationaler und entwicklungsspezifischer Eigenschaften erweisen sich Entwurfstaktikdiagramme als exzellentes Werkzeug. Sie erlauben die Bereitstellung passender Entwurfsstrategien und -taktiken, die sich wiederum oft mithilfe von Entwtufsmustem umsetzen lassen. Ein derart anwendungsgetriebenes Vorgehen verhilft übrigens zu hoher Rückverfolgbarkeit der Anforderungen, womit Architekten dann auch Sensitivity und Tradeoff Points aufspüren sowie Risiken identifizieren können.

Endlich begreift Bob: Es bedarf eines gewissen Handwerkzeugs und einer Systematik, damit aus nichtfunktionalen Eigenschaften nicht nicht—funktionierende Systeme entstehen.

Quellen:
<ul>
	<li>iX Magazin für professionelle Informationstechnik 09/2010, S.114ff</li>
	<li><a href="http://www.amazon.de/Software-Architecture-Practice-SEI-Engineering/dp/0321154959">Software Architecture in Practice</a>, ISBN: 978-0321154958</li>
	<li><a href="http://www.amazon.de/dp/0470697342">Patterns for Fault Tolerant Software</a>, ISBN: 978-0470697344</li>
	<li><a href="http://www.amazon.de/dp/0470858842">Security Patterns: Integrating Security and Systems Engineering</a>, ISBN: 978-0470858844</li>
</ul>
