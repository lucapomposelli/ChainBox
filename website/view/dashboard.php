<?php
/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */

 require_once '../src/config.inc.php';
employeeIsNotLogged();

echo getHeader('Dashboard');

$cList = getCustomersList();
$tGenerated = getToken('g');
$tAssigned = getToken('a');
$tBurned = getToken('b');
?>

    <div class="block block__header">
        <img src="img/logo.svg" srcset="img/logo.svg 1.5x" />
    </div>
    <div class="block block__account">
        Ciao, <?=getEmployeeNameById($_SESSION['userID']); ?><br /><a href="logout.php">Logout</a>
    </div>
    <div class="block block__nav">
        <button class="w3-button w3-blue hover-dark2 w3-margin-right" onclick="show_modal('CG');">Genera tokens</button>
        <button class="w3-button w3-blue hover-dark2 w3-margin-right" onclick="show_modal('CA');">Trasferisci tokens</button>
        <button class="w3-button w3-blue hover-dark2 w3-margin-right" onclick="show_modal('BR');">Brucia tokens</button>
    </div>
    <div class="block block__mmsk">
        <button id="btn_mmsk_connect" class="w3-button w3-blue hover-dark2" data-wallet="">Connetti a MetaMask</button>
        <a href='https://metamask.io/' target="_blank" id="btn_mmsk_install" class="w3-button w3-blue hover-dark2">Installa MetaMask</a>
    </div>
    <div class="block block__sidebar">
        <p>Generati: <?=$tGenerated; ?></p>
		<p>Assegnati: <?=$tAssigned; ?></p>
        <p>Bruciati: <?=$tBurned; ?></p>
		<p>Pending: <?=$tGenerated - $tAssigned; ?></p>
        <hr />
        ETH : <span id="mmsk_balance">-</span>
    </div>
    <div class="block block__main">

        <!-- Contract Generator (CG) -->
        <div id="modal_CG" class="w3-modal">
            <div class="w3-modal-content w3-animate-top w3-card-4">
                <header class="w3-container w3-blue">
                    <span onclick="hide_modal();" class="w3-button w3-large w3-display-topright hover-dark2">×</span>
                    <h2 class="uppercase">Genera tokens</h2>
                </header>
                <div class="w3-container">
                    <form class="w3-padding-24">
                        <!-- FIELD #1 -->
                        <p>
                            <input type="checkbox" id="checkbox_0_CG" data-target="0" data-modal="CG" class="w3-check">
                            <label for="checkbox_0_CG">Genera tokens per FinCode</label>
                        </p>
                        <!-- FIELD #2 -->
                        <p>
                            <label for="selectCustomer_0_CG" class="w3-text-blue">
                                <b>Cliente</b>
                            </label>
                            <select id="selectCustomer_0_CG" name="selectCustomer_0_CG" onchange="getCustomerData();" class="js-example-basic-single js-states form-control" style="width:100%" required>
                                <option></option>
                                <?php echo $cList; ?>
                            </select>
                        </p>
                        <!-- CUSTOMER SUMMARY -->
                        <table class="w3-table w3-striped customer-summary">
                            <tr>
                                <td>Nome e cognome:</td>
                                <td id="c_0_denomination_CG"></td>
                            </tr>
                            <tr>
                                <td>Luogo di nascita:</td>
                                <td id="c_0_birthplace_CG"></td>
                            </tr>
                            <tr>
                                <td>Data di nascita:</td>
                                <td id="c_0_birthdate_CG"></td>
                            </tr>
                            <tr>
                                <td>Societ&agrave;</td>
                                <td id="c_0_company_CG"></td>
                            </tr>
                            <tr>
                                <td>Sede legale:</td>
                                <td id="c_0_address_CG"></td>
                            </tr>
                            <tr>
                                <td>Wallet ETH:</td>
                                <td id="c_0_publickey_CG"></td>
                            </tr>
                            <tr>
                                <td>Numero di token:</td>
                                <td id="c_0_tokens_CG"></td>
                            </tr>
                        </table>
                        <div id="warning_CG" class="w3-panel w3-display-container w3-animate-opacity w3-amber">
                            <p>Il cliente selezionato non ha alcun wallet associato</p>
                        </div>
                        <!-- FIELD #3 -->
                        <p>
                            <label for="inputToken_CG" class="w3-text-blue">
                                <b>Tokens da generare</b>
                            </label>
                            <input type="number" id="inputToken_CG" class="w3-input w3-border" required>
                            <div id="errorToken_CG" class="w3-panel w3-display-container w3-animate-opacity w3-red">
                                <p>Indicare un numero valido di tokens da generare</p>
                            </div>
                        </p>
                        <!-- LOADER -->
                        <div id="loader_CG" class="loader"></div>
                        <div id="loaderText_CG" class="w3-center"></div>
                    </form>
                </div>
                <footer class="w3-container w3-border-top w3-display-container">
                    <div class="w3-bar">
                        <p>
                            <span class="w3-button w3-red hover-dark2" onclick="hide_modal();">Annulla</span>
                            <button type="submit" class="w3-button w3-blue hover-dark2 w3-right" onclick="validateForm();">Genera</button>
                            <form action="#" onSubmit="uploadFiles('myFile'); return false;" method="post" enctype="multipart/form-data" style="float:left;margin-bottom:10px;" class="w3-margin-right">
                                <input type="file" id="myFile" name="filename[]" multiple>
                                <button type="submit" class="w3-button w3-blue hover-dark2">Invia</button>
                            </form>
                        </p>
                    </div>
                </footer>
            </div>
        </div>

        <!-- Contract Associate (CA) -->
        <div id="modal_CA" class="w3-modal">
            <div class="w3-modal-content w3-animate-top w3-card-12">
                <header class="w3-container w3-blue">
                    <span onclick="hide_modal();" class="w3-button w3-large w3-display-topright hover-dark2">×</span>
                    <h2 class="uppercase">Trasferisci token</h2>
                </header>
                <div class="w3-container">
                    <form class="w3-padding-24">
                        <!-- FIELD #1 -->
                        <p>
                            <input type="checkbox" id="checkbox_0_CA" data-target="0" data-modal="CA" class="w3-check">
                            <label for="checkbox_0_CA">Mittente FinCode</label>
                        </p>
                        <!-- FIELD #2 -->
                        <p>
                            <label for="selectCustomer_0_CA" class="w3-text-blue">
                                <b>Mittente</b>
                            </label>
                            <select id="selectCustomer_0_CA" name="selectCustomer_0_CA" onchange="getCustomerData();" class="js-example-basic-single js-states form-control" style="width:100%" required>
                                <option></option>
                                <?php echo $cList; ?>
                            </select>
                        </p>
                        <!-- SENDER SUMMARY -->
                        <table class="w3-table w3-striped customer-summary">
                            <tr>
                                <td>Nome e cognome:</td>
                                <td id="c_0_denomination_CA"></td>
                            </tr>
                            <tr>
                                <td>Luogo di nascita:</td>
                                <td id="c_0_birthplace_CA"></td>
                            </tr>
                            <tr>
                                <td>Data di nascita:</td>
                                <td id="c_0_birthdate_CA"></td>
                            </tr>
                            <tr>
                                <td>Societ&agrave;</td>
                                <td id="c_0_company_CA"></td>
                            </tr>
                            <tr>
                                <td>Sede legale:</td>
                                <td id="c_0_address_CA"></td>
                            </tr>
                            <tr>
                                <td>Wallet ETH:</td>
                                <td id="c_0_publickey_CA"></td>
                            </tr>
                            <tr>
                                <td>Numero di token:</td>
                                <td id="c_0_tokens_CA"></td>
                            </tr>
                        </table>
                        <!-- FIELD #3 -->
                        <p>
                            <input type="checkbox" id="checkbox_1_CA" data-target="1" data-modal="CA" class="w3-check">
                            <label for="checkbox_1_CA">Destinatario FinCode</label>
                        </p>
                        <!-- FIELD #4 -->
                        <p>
                            <label for="selectCustomer_1_CA" class="w3-text-blue">
                                <b>Destinatario</b>
                            </label>
                            <select id="selectCustomer_1_CA" name="selectCustomer_1_CA" onchange="getCustomerData(1);" class="js-example-basic-single js-states form-control" style="width:100%" required>
                                <option></option>
                                <?php echo $cList; ?>
                            </select>
                        </p>
                        <!-- RECIPIENT SUMMARY -->
                        <table class="w3-table w3-striped customer-summary">
                            <tr>
                                <td>Nome e cognome:</td>
                                <td id="c_1_denomination_CA"></td>
                            </tr>
                            <tr>
                                <td>Luogo di nascita:</td>
                                <td id="c_1_birthplace_CA"></td>
                            </tr>
                            <tr>
                                <td>Data di nascita:</td>
                                <td id="c_1_birthdate_CA"></td>
                            </tr>
                            <tr>
                                <td>Societ&agrave;</td>
                                <td id="c_1_company_CA"></td>
                            </tr>
                            <tr>
                                <td>Sede legale:</td>
                                <td id="c_1_address_CA"></td>
                            </tr>
                            <tr>
                                <td>Wallet ETH:</td>
                                <td id="c_1_publickey_CA"></td>
                            </tr>
                            <tr>
                                <td>Numero di token:</td>
                                <td id="c_1_tokens_CA"></td>
                            </tr>
                        </table>
                        <div id="warning_CA" class="w3-panel w3-display-container w3-animate-opacity w3-amber"></div>
                        <div id="errorCustomer" class="w3-panel w3-display-container w3-animate-opacity w3-red"></div>
                        <!-- FIELD #5 -->
                        <p>
                            <label for="inputToken_CA" class="w3-text-blue">
                                <b>Tokens da bruciare</b>
                            </label>
                            <input type="number" id="inputToken_CA" class="w3-input w3-border" required>
                            <div id="errorToken_CA" class="w3-panel w3-display-container w3-animate-opacity w3-red"></div>
                        </p>
                        <!-- LOADER -->
                        <div id="loader_CA" class="loader"></div>
                        <div id="loaderText_CA" class="w3-center"></div>
                    </form>
                </div>
                <footer class="w3-container w3-border-top w3-display-container">
                    <div class="w3-bar">
                        <p>
                            <span class="w3-button w3-red hover-dark2" onclick="hide_modal();">Annulla</span>
                            <button type="submit" class="w3-button w3-blue hover-dark2 w3-right" onclick="validateForm();">Brucia</button>
                            <form action="#" onSubmit="uploadFiles('myFile2'); return false;" method="post" enctype="multipart/form-data" style="float:left;margin-bottom:10px;" class="w3-margin-right">
                                <input type="file" id="myFile2" name="filename[]" multiple>
                                <button type="submit" class="w3-button w3-blue hover-dark2">Invia</button>
                            </form>
                        </p>
                    </div>
                </footer>
            </div>
        </div>

        <!-- Burn (BR) -->
        <div id="modal_BR" class="w3-modal">
            <div class="w3-modal-content w3-animate-top w3-card-4">
                <header class="w3-container w3-blue">
                    <span onclick="hide_modal();" class="w3-button w3-large w3-display-topright hover-dark2">×</span>
                    <h2 class="uppercase">Brucia token</h2>
                </header>
                <div class="w3-container">
                    <form class="w3-padding-24">
                        <!-- FIELD #1 -->
                        <p>
                            <input type="checkbox" id="checkbox_0_BR" data-target="0" data-modal="CA" class="w3-check">
                            <label for="checkbox_0_BR">Mittente FinCode</label>
                        </p>
                        <!-- FIELD #2 -->
                        <p>
                            <label for="selectCustomer_0_BR" class="w3-text-blue">
                                <b>Mittente</b>
                            </label>
                            <select id="selectCustomer_0_BR" name="selectCustomer_0_BR" onchange="getCustomerData();" class="js-example-basic-single js-states form-control" style="width:100%" required>
                                <option></option>
                                <?php echo $cList; ?>
                            </select>
                        </p>
                        <!-- SENDER SUMMARY -->
                        <table class="w3-table w3-striped customer-summary">
                            <tr>
                                <td>Nome e cognome:</td>
                                <td id="c_0_denomination_BR"></td>
                            </tr>
                            <tr>
                                <td>Luogo di nascita:</td>
                                <td id="c_0_birthplace_BR"></td>
                            </tr>
                            <tr>
                                <td>Data di nascita:</td>
                                <td id="c_0_birthdate_BR"></td>
                            </tr>
                            <tr>
                                <td>Societ&agrave;</td>
                                <td id="c_0_company_BR"></td>
                            </tr>
                            <tr>
                                <td>Sede legale:</td>
                                <td id="c_0_address_BR"></td>
                            </tr>
                            <tr>
                                <td>Wallet ETH:</td>
                                <td id="c_0_publickey_BR"></td>
                            </tr>
                            <tr>
                                <td>Numero di token:</td>
                                <td id="c_0_tokens_BR"></td>
                            </tr>
                        </table>
                        <div id="warning_BR" class="w3-panel w3-display-container w3-animate-opacity w3-amber"></div>
                        <div id="errorCustomer_BR" class="w3-panel w3-display-container w3-animate-opacity w3-red"></div>
                        <!-- FIELD #5 -->
                        <p>
                            <label for="inputToken_BR" class="w3-text-blue">
                                <b>Tokens da bruciare</b>
                            </label>
                            <input type="number" id="inputToken_BR" class="w3-input w3-border" required>
                            <div id="errorToken_BR" class="w3-panel w3-display-container w3-animate-opacity w3-red"></div>
                        </p>
                        <!-- LOADER -->
                        <div id="loader_BR" class="loader"></div>
                        <div id="loaderText_BR" class="w3-center"></div>
                    </form>
                </div>
                <footer class="w3-container w3-border-top w3-display-container">
                    <div class="w3-bar">
                        <p>
                            <span class="w3-button w3-red hover-dark2" onclick="hide_modal();">Annulla</span>
                            <button type="submit" class="w3-button w3-blue hover-dark2 w3-right" onclick="validateForm();">Brucia</button>
                        </p>
                    </div>
                </footer>
            </div>
        </div>

        <!-- Alerts -->
        <div id="alerts"></div>

        <!-- Table log -->

        <input type="checkbox" name="logType" id="logType">
        <label for="logType"> Mostra\Nascondi token Burnati</label><br>

        <div id="table"></div>

        <!-- Functions result -->
        <div id="contractResult">
            <h4>Riepilogo</h4>
            <div class="fillTable"></div>
        </div>
    </div>
    <div class="block block__footer">
        © 2021 CM Consulting Network S.p.A.
    </div>

<?php

    // $token = new \Token();
    // $token->getLogsBurned();

    echo loadJQueryScripts(array('select2'));
    echo getFooter('dashboard');
?>

