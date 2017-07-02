<?php
    function createBookies($rowData) {
        // "<a class='bookie-label' href='#' title='" . $row['Bookie_Full'] . "'>" . $row['Bookie_Short']
        $short_names = explode(",", $rowData['Bookie_Short']);
        $long_names = explode(",", $rowData['Bookie_Full']);
        $count = sizeof($short_names);
        $bookie_str = "";
        for($i = 0; $i < $count; $i++) {
            $bookie_str .= "<div class='dropdown bookie-box'><a data-target='#' href='#' data-toggle='dropdown' class='dropdown-toggle'>";
            $bookie_str .= "<span class='bookie-label' title='" . $long_names[$i] . "'>";
            $bookie_str .= $short_names[$i];
            if($i != $count - 1) {
                $bookie_str .= ", ";
            } 
            $bookie_str .= "</span></a>";
            $bookie_str .= "<div class='dropdown-menu bet-place-box'>" . betPlaceBox($rowData) . "</div></div>";
        }
        $bookie_str .= "</div>";
        return $bookie_str;
    }

    function arbDropdown($rowData) {
        $arb_html = "<div class='dropdown arb-button'><a data-target='#' href='#' data-toggle='dropdown' class='dropdown-toggle'>";
        $arb_html .= "<button class='btn btn-danger'>+</button></a>";
        $arb_html .= "<div class='dropdown-menu arb-box'><p>Back " . $rowData['Price'] . " with €10</p>";
        $arb_html .= "<p>Lay " . "(LayPrice)" . " with " . "(LayStake)" . " (liability €" . "((LayPrice - 1)*LayStake)" . "</p>";
        $arb_html .= "To guarantee €" . "(Profit)" . "</div>";
        $arb_html .= "</div>";
        return $arb_html;
    }

    function betPlaceBox($rowData) {
        $box_html = "<div class='row'><div class='col-md-6'><h5><small class='text-muted'>Name</small></h5>" . $rowData['Name'];
        $box_html .= "</div><div class='col-md-6'><h5><span class='text-muted'>Price</small></h5>" . $rowData['Price'] . "</div></div>";
        $box_html .= "<div class='row'><div class='col-md-6'><h5><span class='text-muted'>Venue</small></h5>" . $rowData['Venue'] . "</div>";
        $box_html .= "<div class='col-md-6'><h5><span class='text-muted'>Stake</small></h5>";
        $box_html .= "<div class='input-group'><input type='text' class='form-control'/>";
        $box_html .= "<span class='input-group-btn'><button class='btn btn-secondary' type='button'>Go</button></span>";
        $box_html .= "</div></div></div>";
        return $box_html;
    }
?>
